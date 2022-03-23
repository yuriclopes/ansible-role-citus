# Ansible Role: Citus

[![CI](https://github.com/yuriclopes/ansible-role-citus/workflows/CI/badge.svg?event=push)](https://github.com/yuriclopes/ansible-role-citus/actions?query=workflow%3ACI)

Installs and configures Citus PostgreSQL Cluster server on RHEL/CentOS or Debian/Ubuntu servers.

## Requirements (Debian)
### APT Packages on target hosts
- iproute2
- python3

The inventory should be split in 2 Groups:
    - `coordinator`: Single instance responsible for coordinate worker nodes
    - `worker`: Multiple instances responsible for receive the shards.

```yaml
    - hosts: all
      roles:
        - role: yuriclopes.citus
          become: yes
```

## Role Variables

Available variables are listed in defaults folder (see `defaults/`):

## Dependencies

None.

## Example Playbook

```yaml
    - hosts: all
      roles:
        - role: yuriclopes.citus
          become: yes
```

## License

MIT / BSD

## Author Information

This role was created in 2022 by Yuri Corona Lopes