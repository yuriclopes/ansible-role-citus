#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2022, Yuri Corona Lopes <yuriclopes@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from sqlite3 import DatabaseError
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: citus_worker_node
version_added: "0.1"
short_description: Manages Citus Workers state on Cluster
description:
   - 'Manages Citus Workers state on Cluster'
options:
    coordinator_login_host:
        description:
            - The login host used to authenticate with coordinator node
        required: true
        default: null
    coordinator_login_username:
        description:
            - The login username used to authenticate with coordinator node
        required: false
        default: postgres
    coordinator_login_password:
        description:
            - The login password used to authenticate with coordinator node
        required: false
        default: ''
    coordinator_login_port:
        description:
            - The login port used to authenticate with coordinator node
        required: false
        default: 5432
requirements: [ psycopg2 ]
author: Yuri Corona Lopes <yuriclopes@gmail.com>
'''

DEFAULT_COORDINATOR_USERNAME = "postgres"
DEFAULT_COORDINATOR_PASSWORD = None
DEFAULT_COORDINATOR_PORT = 5432
DEFAULT_WORKER_PORT = 5432

PSYCOPG2_FOUND = False

try:
    import psycopg2
    PSYCOPG2_FOUND = True
except ImportError:
    pass

def connect_to_coordinator(
    module,
    coordinator_host: str,
    database: str,
    coordinator_username: str = DEFAULT_COORDINATOR_USERNAME,
    coordinator_password: str = DEFAULT_COORDINATOR_PASSWORD,
    coordinator_port: int = DEFAULT_COORDINATOR_PORT
    ):
    """ Login on Coordinator Node """
    try:
        conn = psycopg2.connect(
            dbname=database,
            host=coordinator_host,
            port=coordinator_port,
            user=coordinator_username,
            password=coordinator_password
            )
    except psycopg2.Error as error:
        module.fail_json(
            msg=f"Cannot connect with Coordinator node. Code: {error.pgcode} - {error.pgerror}"
        )

    return conn

def check_if_worker_exists(connection, worker_node: str, worker_port: int):
    """ Check if worker node is already present on cluster """
    with connection:
        with connection.cursor() as curs:
            curs.execute("""
                SELECT * FROM citus_get_active_worker_nodes() 
                WHERE node_name = %(worker_node)s 
                AND node_port = %(worker_port)s;
                """,
                {
                    'worker_node': worker_node,
                    'worker_port': worker_port
                }
            )

            return curs.rowcount > 0

def add_worker_node(connection, worker_node: str, worker_port: int):
    """ Check if worker node is already present on cluster """
    with connection:
        with connection.cursor() as curs:
            curs.execute(
                "SELECT * FROM citus_add_node(%(worker_node)s , %(worker_port)s)",
                {
                    'worker_node': worker_node,
                    'worker_port': worker_port
                }
            )

            return curs.rowcount > 0


def main():
    """ Starts Ansible Module """
    module = AnsibleModule(
        argument_spec = dict(
            coordinator_login_host      = dict(type='str'),
            coordinator_login_port      = dict(type='int', default=DEFAULT_COORDINATOR_PORT),
            coordinator_login_user      = dict(default=DEFAULT_COORDINATOR_USERNAME),
            coordinator_login_password  = dict(default=DEFAULT_COORDINATOR_PASSWORD, no_log=True),
            worker_node_host            = dict(type='str'),
            worker_node_port            = dict(type='int', default=DEFAULT_WORKER_PORT),
            database                    = dict(type='str')
        )
    )

    if not PSYCOPG2_FOUND:
        module.fail_json(msg='the python psycopg2 module is required')

    coordinator_login_host      = module.params['coordinator_login_host']
    coordinator_login_port      = module.params['coordinator_login_port']
    coordinator_login_user      = module.params['coordinator_login_user']
    coordinator_login_password  = module.params['coordinator_login_password']
    worker_node_host            = module.params['worker_node_host']
    worker_node_port            = module.params['worker_node_port']
    database                    = module.params['database']

    # connect
    client = connect_to_coordinator(
        module=module,
        coordinator_host = coordinator_login_host,
        coordinator_username = coordinator_login_user,
        coordinator_password = coordinator_login_password,
        coordinator_port = coordinator_login_port,
        database = database
    )

    result = {}
    result['changed'] = False

    if check_if_worker_exists(client, worker_node_host, worker_node_port):
        result['success'] = True
    else:
        result['changed'] = add_worker_node(client, worker_node_host, worker_node_port)
        result['success'] = add_worker_node(client, worker_node_host, worker_node_port)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
