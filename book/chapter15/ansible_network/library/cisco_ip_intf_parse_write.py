#!/usr/bin/python
#coding: utf-8 -*-

import yaml
FILENAME="group_vars/cisco-devices/all.yml"

class FactUpdater(object):

    def __init__(self, module):
        self.intf = module.params['ipTable']
        self.hostname = module.params['hostname']
        self.file_content = {'host2intf':{}}
        #self.FILENAME="group_vars/ints_"+self.hostname+'.yml'

    def read(self):
        try:
            with open(FILENAME, 'r') as fileObj:
                self.file_content = yaml.load(fileObj)
        except:
            # in case there is no file - create it
            open(FILENAME, 'w').close()

    def write(self):
        with open(FILENAME, 'w') as fileObj:
            yaml.dump(self.file_content, fileObj, explicit_start=True, indent=2)


    def update(self):
        #if not self.file_content:
        if not self.file_content or not 'host2intf' in self.file_content:
            self.file_content = {'host2intf':{}}
        self.file_content['host2intf'][self.hostname] = self.intf



def main():
    module = AnsibleModule(
        argument_spec=dict(
            ipTable=dict(required=True, type='list'),
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
