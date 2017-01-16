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


for intf in sw1_fast_int['access']:
    print 'interface FastEthernet' + intf
    for command in sw_int_templates.access_template:
        if command.endswith('access vlan'):
            print ' %s %s' % (command, sw1_fast_int['access'][intf])
        else:
            print ' %s' % command
```

Вывод мы получаем такой же:
```
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
```

В этом примере мы увидели:
* как импортировать модули
* что модули - это обычные файлы с кодом Python
* что мы можем импортировать все объекты модуля (import module)
* или только некоторые (from module import object)


### if __name__ == "__main__"

Иногда, скрипт, который вы создали, может выполняться самостоятельно, а может быть импортирован как модуль, другим скриптом.

На основе файла generate_sw_conf.py создадим новый файл generate_sw_conf2.py.
```python
import sw_int_templates
from sw1 import sw1_fast_int


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

Отличия:
* цикл for перенесен в функцию
* вместо print, мы добавляем строки в список result
* функция возвращает полученный список

В последней строке мы выводим полученный результат. Вывод будет таким же:
```
$ python generate_sw_conf2.py
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

А теперь создадим новый файл generate_cfg_sw2.py:
```python
import sw_int_templates
from sw2 import sw2_fast_int
from generate_sw_conf2 import generate_access_cfg


print '\n'.join(generate_access_cfg(sw2_fast_int))
```

В нем мы импортируем шаблон, затем словарь с информацией о коммутаторе (sw2_fast_int) и, последнее, импортируем функцию generate_access_cfg из файла generate_sw_conf2.py.

Файл sw2.py:
```python
sw2_fast_int = {
                'access':{
                         '0/10':'20',
                         '0/12':'21',
                         '0/13':'27',
                         '0/14':'50'}}

```


Попробуем выполнить скрипт:
```
$ python generate_cfg_sw2.py
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
interface FastEthernet0/10
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/12
 switchport mode access
 switchport access vlan 21
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/13
 switchport mode access
 switchport access vlan 27
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 spanning-tree bpduguard enable
```

Обратите внимание, что мы получили конфигурацию для 8 портов.
Хотя, в файле sw2.py в словаре всего 4 порта.

Так получилось из-за строки print в файле generate_sw_conf2.py:
```
print '\n'.join(generate_access_cfg(sw1_fast_int))
```

Когда мы импортируем какой-то модуль, всё, что находится в модуле, выполняется.
И, так как в данном случае, мы выводим информацию на стандартный поток вывод с помощью print,
мы видим результат выполнения выражения из файла generate_sw_conf2.py, когда запускаем файл generate_cfg_sw2.py.

В Python есть специальный прием, который позволяет указать, что какой-то код должен выполняться, только когда файл запускается напрямую.

Файл generate_sw_conf2.py:
```python
import sw_int_templates
from sw1 import sw1_fast_int


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

Если мы запустим скрипт generate_sw_conf2.py, конфигурация будет выводиться:
```python
$ python generate_sw_conf2.py
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

Но теперь, когда мы запускаем скрипт generate_cfg_sw2.py, print из файла generate_sw_conf2.py не выводится:
```python
$ python generate_cfg_sw2.py
interface FastEthernet0/10
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/12
 switchport mode access
 switchport access vlan 21
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/13
 switchport mode access
 switchport access vlan 27
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 spanning-tree bpduguard enable
```


