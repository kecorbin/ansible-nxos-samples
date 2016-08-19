#!/usr/bin/python
#
#  A simple Ansible custom module to deploy BGP on NX-OS switches
#

DOCUMENTATION = '''
---

module: nxos_bgp
version_added: "0.1"
short_description: Manages BGP peering
description:
    - Manages BGP peers on NX-OS switches
author: Kevin Corbin @kecorbin
options:
    asn:
        description:
            - Autonomous System Number
    neighbor_id:
        description:
            - Peer IP address
        required: true
        default: null
    vrf:
        description:
            - VRF for this neighbor
        requred: false
        default: default (Global Routing Table)
    remote_as:
        description:
            - Administrative state of the interface
        required: true
        default: up
        choices: ['up','down']

'''

EXAMPLES = '''
# Ensure iBGP neightbor 1.1.1.1 exists on all hosts
- nxos_bgp: asn=65535 neighbor-id=1.1.1.1 remote-as=65535 host={{ inventory_hostname }}

'''

# TODO update this

RETURN = '''

proposed:
    description: k/v pairs of neighbor parameters passed into module
    returned: always
    type: dict
    sample:
existing:
    description: list of k/v pairs of existing neighbors
    type: list
    sample:
end_state:
    description: k/v pairs of neighbors after module execution
    returned: always
    type: dict or null
    sample:
state:
    description: state as sent in from the playbook
    returned: always
    type: string
    sample: "present"
updates:
    description: command list sent to the device
    returned: always
    type: list
    sample: SAMPLE NEEDED
changed:
    description: check to see if a change was made on the device
    returned: always
    type: boolean
    sample: true

'''

def execute_config_command(commands, module):
    try:
        module.configure(commands)
    except ShellError, clie:
        module.fail_json(msg='Error sending CLI commands',
                         error=str(clie), commands=commands)

def main():
    argument_spec = dict(
        asn=dict(required=True, ),
        neighbor_id=dict(required=True, ),
        remote_as=dict(required=True, ),
        vrf=dict(default='default', required=False),

    )

    module = get_module(argument_spec=argument_spec,
                        supports_check_mode=True)

    asn = module.params['asn']
    neighbor_id = module.params['neighbor_id']
    remote_as = module.params['remote_as']
    vrf = module.params['vrf']

    args = dict(asn=remote_as, vrf=vrf, neighbor_id=neighbor_id, remote_as=remote_as)

    proposed = {
        "neighbor_id": neighbor_id,
        "vrf": vrf,
        "remote_as": remote_as,

    }

    # TODO Determine if we really need to add a neighbor, for now we'll assume so
    existing_neighbors = dict()

    changed = True

    commands = []

    if changed:
        proc_cmd = 'router bgp {}'.format(asn)
        commands.append(proc_cmd)

        if vrf != 'default':
            vrf_cmd = 'vrf {}'.format(vrf)
            commands.append(vrf_cmd)
        else:
            pass

        neighbor_command = 'neighbor {} remote-as {}'.format(neighbor_id, remote_as)
        commands.append(neighbor_command)

        execute_config_command(commands, module)

    # Build results to be returned
    results = dict()
    results['proposed'] = proposed
    results['existing'] = existing_neighbors
    results['changed'] = "changed"

    module.exit_json(**results)



from ansible.module_utils.shell import *
from ansible.module_utils.netcfg import *
from ansible.module_utils.nxos import *

if __name__ == '__main__':
    main()
