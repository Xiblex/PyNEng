# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TEMPLATE_DIR, template = sys.argv[1].split('/')
routers_info = sys.argv[2]

env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))
template = env.get_template(template)

routers = csv.DictReader(open(routers_info))

for router in routers:
    r1_conf = router['name']+'_r1.txt'
    with open(r1_conf,'w') as f:
        f.write(template.render( router ))

