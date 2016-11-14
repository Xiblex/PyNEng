# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('router_template.txt')

with open('routers_info.txt','r') as file:
    data = [line.strip().split(',') for line in file]

routers = [dict(zip(data[0],i)) for i in data[1:]]

for router in routers:
    r1_conf = router['name']+'_r1'
    with open(r1_conf,'w') as f:
        f.write(template.render( router ))

