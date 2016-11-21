#!/usr/bin/python
#coding: utf-8 -*-

# Example from:
# http://networkop.github.io/blog/2015/06/24/ansible-intro/
# http://networkop.github.io/blog/2015/07/03/parser-modules/

class SIIBparse(object):

    def __init__(self, module):
        self.output_text = module.params['output_text']
        self.ip2intf = dict()

    def parse(self):
        for line in self.output_text.split("\n"):
            row = line.split()
            if len(row) > 0 and row[-1] == 'up':
                ipAddress = row[1]
                intfName = row[0]
                self.ip2intf[ipAddress] = intfName
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
