## Распаковка переменных

Распаковка переменных - это специальный синтаксис, который позволяет присваивать переменным элементы итерируемого объекта.

> Достаточно часто этот функционал встречается под именем tuple unpacking. Но распаковка работает на любом итерируемом объекте, не толко с кортежами

Пример распаковки переменных:
```python
In [6]: interface = ['FastEthernet0/1', '10.1.1.1', 'up', 'up']

In [7]: intf, ip, status, protocol = interface

In [8]: intf
Out[8]: 'FastEthernet0/1'

In [9]: ip
Out[9]: '10.1.1.1'
```

Такой вариант намного удобней использовать, чем использование индексов:
```python
In [10]: intf, ip, status, protocol = interface[0], interface[1], interface[2], interface[3]
```

При распаковке переменных, каждый элемент списка попадает в соответствующую переменную.
Но, важно учитывать, что переменных слева должно быть ровно столько, сколько элементов в списке.

Если переменных больше или меньше, возникнет исключение:
```python
In [11]: intf, ip, status = interface
------------------------------------------------------------
ValueError                 Traceback (most recent call last)
<ipython-input-11-a304c4372b1a> in <module>()
----> 1 intf, ip, status = interface

ValueError: too many values to unpack (expected 3)

In [12]: intf, ip, status, protocol, other = interface
------------------------------------------------------------
ValueError                 Traceback (most recent call last)
<ipython-input-12-ac93e78b978c> in <module>()
----> 1 intf, ip, status, protocol, other = interface

ValueError: not enough values to unpack (expected 5, got 4)

```


### Замена ненужных элементов ```_```

Достаточно часто из всех элементов итерируемого объекта, нужны только некоторые.
Но, выше был пример того, что синтаксис распаковки требует указать ровно столько переменных, сколько элементов в итерируемом объекте.

Если, например, из строки line надо получить только VLAN, MAC и интерфейс, надо все равно указать переменную для типа записи:
```python
In [13]: line = '100    01bb.c580.7000    DYNAMIC     Gi0/1'

In [14]: vlan, mac, item_type, intf = line.split()

In [15]: vlan
Out[15]: '100'

In [16]: intf
Out[16]: 'Gi0/1'
```

Но, если тип записи не нужен в дальнейшем, можно заменить переменную item_type нижним подчеркиванием:
```python
In [17]: vlan, mac, _, intf = line.split()
```

Таким образом явно указывается то, что этот элемент не нужен.


Нижнее подчеркивание можно использовать и несколько раз:
```python
In [18]: dhcp = '00:09:BB:3D:D6:58   10.1.10.2        86250       dhcp-snooping   10    FastEthernet0/1'

In [19]: mac, ip, _, _, vlan, intf = dhcp.split()

In [20]: mac
Out[20]: '00:09:BB:3D:D6:58'

In [21]: vlan
Out[21]: '10'

```

### Использование ```*```

Распаковка переменных поддерживает специальный синтаксис, который позволяет распаковывать несколько элементов в один.
Если поставить ```*``` перед именем переменной, в нее запишутся все элементы, кроме тех, что присвоены явно.

Например, так можно получить первый элемент в переменную first, а остальные в rest:
```python
In [22]: vlans = [10, 11, 13, 30]

In [23]: first, *rest = vlans

In [24]: first
Out[24]: 10

In [25]: rest
Out[25]: [11, 13, 30]
```

При этом, переменная со звездочкой всегда будет содержать список:
```python
In [26]: vlans = (10, 11, 13, 30)

In [27]: first, *rest = vlans

In [28]: first
Out[28]: 10

In [29]: rest
Out[29]: [11, 13, 30]
```

Если элемент всего один, в данном случае, распаковка все равно отработает:
```python
In [32]: first, *rest = vlans

In [34]: first
Out[34]: 55

In [35]: rest
Out[35]: []
```

Такая переменная со звездочкой может быть только одна, в выражении распаковки.
```python
In [36]: vlans = (10, 11, 13, 30)

In [37]: first, *rest, *others = vlans
  File "<ipython-input-37-dedf7a08933a>", line 1
    first, *rest, *others = vlans
                                 ^
SyntaxError: two starred expressions in assignment
```

И конечно же, такая переменная может находиться не только в конце выражения:
```python
In [38]: vlans = (10, 11, 13, 30)

In [39]: *rest, last = vlans

In [40]: rest
Out[40]: [10, 11, 13]

In [41]: last
Out[41]: 30
```

Таким образом можно указать, что нужен первый, второй и послений элемент:
```python
In [42]: cdp = 'SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1'

In [43]: name, l_intf, *other, r_intf = cdp.split()

In [44]: name
Out[44]: 'SW1'

In [45]: l_intf
Out[45]: 'Eth'

In [46]: r_intf
Out[46]: '0/1'
```

### Примеры распаковки

#### Распаковка итерируемых объектов

Эти примеры показывают, что распаковывать можно не только списки, кортежи и строки, но и любой другой итерируемый объект.

Распаковка range:
```python
In [47]: first, *rest = range(1,6)

In [48]: first
Out[48]: 1

In [49]: rest
Out[49]: [2, 3, 4, 5]
```

Распаковка zip:
```python
In [50]: a = [1,2,3,4,5]

In [51]: b = [100,200,300,400,500]

In [52]: zip(a, b)
Out[52]: <zip at 0xb4df4fac>

In [53]: list(zip(a, b))
Out[53]: [(1, 100), (2, 200), (3, 300), (4, 400), (5, 500)]

In [54]: first, *rest, last = zip(a, b)

In [55]: first
Out[55]: (1, 100)

In [56]: rest
Out[56]: [(2, 200), (3, 300), (4, 400)]

In [57]: last
Out[57]: (5, 500)
```


#### Пример распаковки в цикле for

Пример цикла, который проходится по ключам:
```python
In [58]: access_template = ['switchport mode access',
    ...:                    'switchport access vlan',
    ...:                    'spanning-tree portfast',
    ...:                    'spanning-tree bpduguard enable']
    ...:

In [62]: access = {'0/12':10,
    ...:           '0/14':11,
    ...:           '0/16':17}
    ...:

In [63]: for intf in access:
    ...:     print('interface FastEthernet' + intf)
    ...:     for command in access_template:
    ...:         if command.endswith('access vlan'):
    ...:             print(' {} {}'.format(command, access[intf]))
    ...:         else:
    ...:             print(' {}'.format(command))
    ...:
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

Вместо этого, можно проходиться по парам ключ, значение и сразу же распаковывать их в разные переменные:
```python
In [64]: for intf, vlan in access.items():
    ...:     print('interface FastEthernet' + intf)
    ...:     for command in access_template:
    ...:         if command.endswith('access vlan'):
    ...:             print(' {} {}'.format(command, vlan))
    ...:         else:
    ...:             print(' {}'.format(command))
    ...:
```

Пример распаковки элементов списка в цикле:
```python
In [69]: table
Out[69]:
[['100', 'a1b2.ac10.7000', 'DYNAMIC', 'Gi0/1'],
 ['200', 'a0d4.cb20.7000', 'DYNAMIC', 'Gi0/2'],
 ['300', 'acb4.cd30.7000', 'DYNAMIC', 'Gi0/3'],
 ['100', 'a2bb.ec40.7000', 'DYNAMIC', 'Gi0/4'],
 ['500', 'aa4b.c550.7000', 'DYNAMIC', 'Gi0/5'],
 ['200', 'a1bb.1c60.7000', 'DYNAMIC', 'Gi0/6'],
 ['300', 'aa0b.cc70.7000', 'DYNAMIC', 'Gi0/7']]


In [71]: for line in table:
    ...:     vlan, mac, _, intf = line
    ...:     print(vlan, mac, intf)
    ...:
100 a1b2.ac10.7000 Gi0/1
200 a0d4.cb20.7000 Gi0/2
300 acb4.cd30.7000 Gi0/3
100 a2bb.ec40.7000 Gi0/4
500 aa4b.c550.7000 Gi0/5
200 a1bb.1c60.7000 Gi0/6
300 aa0b.cc70.7000 Gi0/7
```

Но еще лучше сделать так:
```python
In [70]: for vlan, mac, _, intf in table:
    ...:     print(vlan, mac, intf)
    ...:
100 a1b2.ac10.7000 Gi0/1
200 a0d4.cb20.7000 Gi0/2
300 acb4.cd30.7000 Gi0/3
100 a2bb.ec40.7000 Gi0/4
500 aa4b.c550.7000 Gi0/5
200 a1bb.1c60.7000 Gi0/6
300 aa0b.cc70.7000 Gi0/7
```

### Дополнительные материалы

* [Ответ на stackoverflow с множеством вариантов распаковки](https://stackoverflow.com/questions/6967632/unpacking-extended-unpacking-and-nested-extended-unpacking)
* [PEP 3132 -- Extended Iterable Unpacking](https://www.python.org/dev/peps/pep-3132/)

