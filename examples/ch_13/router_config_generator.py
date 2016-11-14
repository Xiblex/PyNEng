# -*- coding: utf-8 -*-
from jinja2 import Template
from router_template import template_r1
from routers_info import routers

for router in routers:
    r1_conf = router['name']+'_r1'
    with open(r1_conf,'w') as f:
        f.write(template_r1.render( router ))
