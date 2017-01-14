#!/usr/bin/env python
# -*- coding: utf-8 -*-

from netmiko import ConnectHandler
import sys

ip, config = sys.argv[1:]

router = {'device_type': 'cisco_ios',
           'username':'python',
           'password':'python',
           'secret':'cisco'}

router['ip'] = ip

ssh = ConnectHandler(**router)
ssh.enable()

config_commands = []

with open(config) as f:
    config_commands.extend(f.readlines())

output2 = ssh.send_config_set(config_commands)

errors = 'Invalid input'
write_errors = []

for line in output2.split('\n'):
    if '#' in line:
        command_line = line
    if errors in line:
        write_errors.append("\nERROR in line", command_line)

if write_errors:
    with open('configs/errors_in_session_'+ip, 'w') as f:
        f.write('\n'.join(write_errors))
