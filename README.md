# ansible-nxos-samples

Ansible playbooks which easily demonstrate various functionality of Ansible + NX-OS based switches

# Overview

The goal of these playbooks is to easily demonstrate the following functionality:

* Core modules - nxos_command, nxos_config, nxos_interface, nxos_bgp nxos_feature, nxos_ip_interface, nxos_vrf, nxos_vrf_interface
* Prompt for variable input
* Global/Shared variables
* Host/Group Variables
* Custom modules - [nxos_bgp](library/nxos_bgp.py)

# Requirements

* python
* virtualenv
* pip
* ansible

# Installation

## Downloading

If you have git installed, clone the repository

    git clone https://github.com/kecorbin/ansible-playbook-samples.git

    cd ansible-playbook-samples

## Usage

1. Modify the [.ansible_env](.ansible_env) file and change *ANSIBLE_NET_USERNAME* and *ANSIBLE_NET_PASSWORD* with appropriate names
2. Modify ansible [hosts](hosts) file and add your switches
3. Execute the following commands

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
source .ansible_enviornment
ansible-playbook -i hosts deploy.yml
```

You will be prompted for a "change record" this can currently be anything you like and is used to stage a rollback checkpoint on the switches.  To rollback
your switches run the following command and enter the same value when prompted.

```
ansible-playbook -i hosts rollback.yml
```


# Next Steps

Explore the roles/deployed/tasks/main.yml and host_vars/* files and modify for your own use cases!!


