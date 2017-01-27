from parse_dhcp_snooping import parser, get

args = parser.parse_args(['get', '-k', 'vlan', '-v', '10'])
print args

get(args)
