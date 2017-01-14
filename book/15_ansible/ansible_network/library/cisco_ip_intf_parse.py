#!/usr/bin/python
#coding: utf-8 -*-
import textfsm


class SIIBparse(object):

    def __init__(self, module):
        self.output_text = module.params['output_text']
        self.ip2intf = list()

    def parse(self):
        template = '/home/nata/day6/ansible/templates/cisco_ios_show_ip_int_brief.template'
        f = open(template, 'r')
        re_table = textfsm.TextFSM(f)
        header = re_table.header
        data = re_table.ParseText(self.output_text)
        self.ip2intf = [ dict(zip(header,v)) for v in data ]

        result = {
            "IPs": self.ip2intf
        }
        rc = 0 if len(self.ip2intf) > 0 else 1
        return rc, result

def main():
    module = AnsibleModule(
        argument_spec=dict(
            output_text=dict(required=True, type='str')
        )
    )
    siib = SIIBparse(module)
    rc, result = siib.parse()
    if rc != 0:
        module.fail_json(msg="Failed to parse. Incorrect input.")
    else:
        module.exit_json(changed=False, ansible_facts=result)

# import module snippets
from ansible.module_utils.basic import *
main()
