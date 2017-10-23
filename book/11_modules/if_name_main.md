## ```if __name__ == "__main__"```

Иногда скрипт, который вы создали, может выполняться и самостоятельно, и может быть импортирован как модуль другим скриптом.

Добавим ещё один скрипт к предыдущему примеру, который будет импортировать функцию из файла generate_sw_int_cfg.py.

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

В файле generate_sw_cfg.py импортируются шаблоны из sw_cfg_templates.py и функции из предыдущих файлов:
```python
from sw_data import sw1_fast_int
from generate_sw_int_cfg import generate_access_cfg
from sw_cfg_templates import basic_cfg, lines_cfg


print(basic_cfg)
print('\n'.join(generate_access_cfg(sw1_fast_int)))
print(lines_cfg)
```

В результате должны отобразиться такие части конфигурации, по порядку:
шаблон basic_cfg, настройка интерфейсов, шаблон lines_cfg.


> Обратите внимание, что из файла можно импортировать несколько объектов:
>```python
>from sw_cfg_templates import basic_cfg, lines_cfg
>```

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


Полученный вывод не совсем правильный: перед строками шаблона basic_cfg идет лишняя конфигурация интерфейсов.


Так получилось из-за строки print в файле generate_sw_int_cfg.py:
```python
print('\n'.join(generate_access_cfg(sw1_fast_int)))
```

Когда скрипт импортирует какой-то модуль, всё, что находится в модуле, выполняется.
И, так как в данном случае, в файле generate_sw_int_cfg.py есть строка с print, на стандартный поток вывода попадает результат выполнения этого выражения при запуске файла generate_sw_int_cfg.py.

В Python есть специальный прием, который позволяет указать, что какой-то код должен выполняться, только когда файл запускается напрямую.

Файл generate_sw_int_cfg2.py:
```python
import sw_int_templates
from sw_data import sw1_fast_int


def generate_access_cfg(sw_dict):
    result = []
    for intf, vlan in sw_dict['access'].items():
        result.append('interface FastEthernet' + intf)
        for command in sw_int_templates.access_template:
            if command.endswith('access vlan'):
                result.append(' {} {}'.format(command, vlan))
            else:
                result.append(' {}'.format(command))
    return result

if __name__ == '__main__':
    print('\n'.join(generate_access_cfg(sw1_fast_int)))

```

Обратите внимание на запись:
```python
if __name__ == '__main__':
    print('\n'.join(generate_access_cfg(sw1_fast_int)))
```

Переменная ```__name__``` - это специальная переменная, которая выставляется равной ```"__main__"```, если файл запускается как основная программа, и выставляется равной имени модуля, если модуль импортируется.

Таким образом, условие ```if __name__ == '__main__'``` проверяет, был ли файл запущен напрямую.

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

