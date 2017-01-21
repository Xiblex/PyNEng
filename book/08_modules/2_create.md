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

И файл sw_data.py:
```python
sw1_fast_int = {
                'access':{
                         '0/12':'10',
                         '0/14':'11',
                         '0/16':'17'}}
```

Теперь попробуем совместить все вместе в файле generate_sw_int_cfg.py:
```python
import sw_int_templates
from sw_data import sw1_fast_int


def generate_access_cfg(sw_dict):
    result = []
    for intf in sw_dict['access']:
        result.append('interface FastEthernet' + intf)
        for command in sw_int_templates.access_template:
            if command.endswith('access vlan'):
                result.append(' %s %s' % (command, sw_dict['access'][intf]))
            else:
                result.append(' %s' % command)
    return result


print '\n'.join(generate_access_cfg(sw1_fast_int))

```

В первых двух строках мы импортируем объекты из других файлов:
* ```import sw_int_templates``` - мы импортируем всё из файла
 * пример использования одного из шаблонов: ```sw_int_templates.access_template```
* ```from sw_data import sw1_fast_int``` - из модуля sw_data мы импортируем только sw1_fast_int
 * при таком импорте, мы можем напрямую обращаться к имени sw1_fast_int

Вывод мы получаем такой:
```
$ python generate_sw_int_cfg.py
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
```

В этом примере мы увидели:
* как импортировать модули
* что модули - это обычные файлы с кодом Python
* что мы можем импортировать все объекты модуля (import module)
* или только некоторые (from module import object)


### ```if __name__ == "__main__"```

Иногда, скрипт, который вы создали, может выполняться и самостоятельно, и может быть импортирован как модуль, другим скриптом.

До сих пор, файл generate_sw_int_cfg.py вызывался самостоятельно.
Теперь мы добавим ещё один скрипт, который будет импортировать функцию из этого файла.

Файл sw_cfg_templates.py с шаблонами конфигурации:
```python
basic_cfg = """
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
"""

lines_cfg = """
!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!
"""
```

То есть, в нем находятся просто строки с конфигурацией, которая всегда одинаковая.

В файле generate_sw_cfg.py мы импортируем и эти шаблоны, и предыдущий файл:
```python
from sw_data import sw1_fast_int
from generate_sw_int_cfg import generate_access_cfg
from sw_cfg_templates import basic_cfg, lines_cfg


print basic_cfg
print '\n'.join(generate_access_cfg(sw1_fast_int))
print lines_cfg
```
То есть, должны отобразиться такие части конфигурации, по порядку:
шаблон basic_cfg, настройка интерфейсов, шаблон lines_cfg.


Обратите внимание, что из файла можно импортировать несколько объектов:
```python
from sw_cfg_templates import basic_cfg, lines_cfg
```

Результат выполнения:
```
$ python generate_sw_cfg.py
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

service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!

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

!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!
```


Мы получили не такой вывод, как ожидали.
Перед строками шаблона basic_cfg, идет лишняя конфигурация интерфейсов.


Так получилось из-за строки print в файле generate_sw_int_cfg.py:
```python
print '\n'.join(generate_access_cfg(sw1_fast_int))
```

Когда мы импортируем какой-то модуль, всё, что находится в модуле, выполняется.
И, так как в данном случае, мы выводим информацию на стандартный поток вывод с помощью print,
мы видим результат выполнения выражения из файла generate_sw_int_cfg.py, когда запускаем файл generate_sw_int_cfg.py.

В Python есть специальный прием, который позволяет указать, что какой-то код должен выполняться, только когда файл запускается напрямую.

Файл generate_sw_int_cfg2.py:
```python
import sw_int_templates
from sw_data import sw1_fast_int


def generate_access_cfg(sw_dict):
    result = []
    for intf in sw_dict['access']:
        result.append('interface FastEthernet' + intf)
        for command in sw_int_templates.access_template:
            if command.endswith('access vlan'):
                result.append(' %s %s' % (command, sw_dict['access'][intf]))
            else:
                result.append(' %s' % command)
    return result

if __name__ == "__main__":
    print '\n'.join(generate_access_cfg(sw1_fast_int))

```

Обратите внимание на запись:
```python
if __name__ == "__main__":
    print '\n'.join(generate_access_cfg(sw1_fast_int))
```

Переменная ```__name__``` это специальная переменная, которая выставляется равной ```"__main__"```, если если файл запускается как основная программа.
И выставляется равной имени модуля, если модуль импортируется.

Таким образом, условие ```if __name__ == "__main__"``` проверяет был ли файл запущен напрямую.

Измените в файле generate_sw_cfg.py строку:
```python
from generate_sw_int_cfg import generate_access_cfg
```

на строку:
```python
from generate_sw_int_cfg2 import generate_access_cfg
```

И попробуйте запустить скрипт:
```python
$ python generate_sw_cfg.py

service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!

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

!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!

```

Теперь print из файла generate_sw_int_cfg2.py не выводится.
