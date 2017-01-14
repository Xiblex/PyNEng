import sw_int_templates
from sw1 import sw1_fast_int


for int in sw1_fast_int['access']:
    print 'interface FastEthernet' + int
    for command in sw_int_templates.access_template:
        if command.endswith('access vlan'):
            print ' %s %s' % (command, sw1_fast_int['access'][int])
        else:
            print ' %s' % command

"""
Example:

$ python generate_sw_conf.py
interface FastEthernet0/12
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 11
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/16
 switchport mode access
 switchport access vlan 17
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/17
 switchport mode access
 switchport access vlan 150
 spanning-tree portfast
 spanning-tree bpduguard enable
"""
