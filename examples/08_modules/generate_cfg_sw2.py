import sw_int_templates
from sw2 import sw2_fast_int
from generate_sw_conf2 import generate_access_cfg



print '\n'.join(generate_access_cfg(sw2_fast_int))
