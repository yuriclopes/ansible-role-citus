# Ansible Role: Citus

[![Molecule](https://github.com/yuriclopes/ansible-role-citus/actions/workflows/ci.yml/badge.svg)](https://github.com/yuriclopes/ansible-role-citus/actions/workflows/ci.yml)

Installs and configures Citus PostgreSQL Cluster server on RHEL/CentOS or Debian/Ubuntu servers.

## Requirements (Debian)

### APT Packages on Debian target hosts
- iproute2
- python3

### RPM Packages on RHEL target hosts
- iproute
- python3

The inventory should be split in 2 Groups:
    - `coordinator`: Single instance responsible for coordinate worker nodes
    - `worker`: Multiple instances responsible for receive the shards.

```yaml
    - hosts: citus
      become: yes
      roles:
        - role: yuriclopes.citus
```

## Role Variables

Additional variables listed below. Available variables are listed in defaults folder (see `defaults/`):

| Variable | Description | Required | Type | Default |
|----------|-------------|----------|------|---------|
|`postgres_password` | Password to be setted to postgres user | `yes` | `str` | null |
|`worker_dns` | Worker Node DNS Recordset to be used instead ip | `no` | `str` | Node Private IP |
|`coordinator_dns` | Coordinator Node DNS Recordset to be used instead ip | `no` | `str` | Node Private IP |

## Dependencies

### PIP Packages (requirements.txt)
- netaddr>=0.7.0

## Example Playbook

```yaml
    - hosts: citus
      become: yes
      roles:
        - role: yuriclopes.citus
```

## License

MIT / BSD

## Author Information

This role was created in 2022 by Yuri Corona Lopes