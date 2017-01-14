#!/usr/bin/python
#coding: utf-8 -*-

# Example from:
# http://networkop.github.io/blog/2015/06/24/ansible-intro/
# http://networkop.github.io/blog/2015/07/03/parser-modules/

import yaml
FILENAME="group_vars/all.yml"

class FactUpdater(object):

    def __init__(self, module):
        self.ip2intf = module.params['ipTable']
        self.hostname = module.params['hostname']
        self.file_content = {'ip2host':{}}

    def read(self):
        try:
            with open(FILENAME, 'r') as fileObj:
                self.file_content = yaml.load(fileObj)
        except:
            # in case there is no file - create it
            open(FILENAME, 'w').close()

    def write(self):
        with open(FILENAME, 'w') as fileObj:
            yaml.safe_dump(self.file_content, fileObj, explicit_start=True, indent=2, allow_unicode=True)


    def update(self):
        if not 'ip2host' in self.file_content:
            self.file_content['ip2host'] = dict()
        for ip in self.ip2intf:
            self.file_content['ip2host'][ip] = [self.hostname, self.ip2intf[ip]]



def main():
    module = AnsibleModule(
        argument_spec=dict(
            ipTable=dict(required=True, type='dict'),
            hostname=dict(required=True, type='str'),
        )
    )
    result = ''
    factUpdater = FactUpdater(module)
    try:
        factUpdater.read()
        factUpdater.update()
        factUpdater.write()
    except IOError as e:
        module.fail_json(msg="Unexpected error: " + str(e))

    module.exit_json(changed=False)

# import module snippets
from ansible.module_utils.basic import *
main()
