## Создание своих модулей
Так как модуль это просто файл с расширение .py и кодом Python, мы можем легко создать несколько своих модулей.

Попробуем, для примера, использовать скрипт из раздела "Совмещение for и if". Разнесем шаблоны портов, данные и формирование команд в разные файлы.

Например, у нас есть файл sw_int_templates.py:
```python
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk allowed vlan']

l3int_template = ['no switchport', 'ip address']
```

И файл sw1.py:
```python
sw1_fast_int = {
                'access':{
                         '0/12':'10',
                         '0/14':'11',
                         '0/16':'17',
                         '0/17':'150'}}
```

Теперь попробуем совместить все вместе в файле generate_sw_conf.py:
```python
import sw_int_templates
from sw1 import sw1_fast_int


for int in sw1_fast_int['access']:
    print 'interface FastEthernet' + int
    for command in sw_int_templates.access_template:
        if command.endswith('access vlan'):
            print ' %s %s' % (command, sw1_fast_int['access'][int])
        else:
            print ' %s' % command
```

Вывод мы получаем такой же:
```python
nata$ python generate_sw_conf.py
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
```

В этом примере мы увидели:
* как импортировать модули
* что модули - это обычные файлы с кодом Python
* что мы можем импортировать все объекты модуля (import module)
* или только некоторые (from module import object)
