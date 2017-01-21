## Распаковка аргументов

Мы рассмотрели как создавать параметры функции, которые могут принимать аргументы переменной длинны.
Но в Python, выражения ```*args``` и ```**kwargs``` позволяют выполнять ещё одну задачу - распаковку аргументов.

До сих пор, мы вызывали вызывали функции самостоятельно, вручную.
И, соответственно, передавали все нужные аргументы.

Но, в реальной жизни, мы, как правило, получаем откуда-то данные и должны передать их в функцию программно.
И часто данные идут в виде какого-то объекта Python.

### Распаковка позиционных аргументов

Например, у нас есть функция config_interface (файл func_args_var_unpacking.py): 
```python
def config_interface(intf_name, ip_address, cidr_mask):
    interface = 'interface %s'
    no_shut = 'no shutdown'
    ip_addr = 'ip address %s %s'
    result = []
    result.append(interface % intf_name)
    result.append(no_shut)

    mask_bits = int(cidr_mask.split('/')[-1])
    bin_mask = '1'*mask_bits + '0'*(32-mask_bits)
    dec_mask = '.'.join([ str(int(bin_mask[i:i+8], 2)) for i in [0,8,16,24] ])

    result.append(ip_addr % (ip_address, dec_mask))
    return result
```

Функция ожидает как аргумент:
* intf_name - имя интерфейса
* ip_address - IP-адрес
* cidr_mask - маску в формате CIDR (допускается и формат /24 и просто 24)

На выходе, она выдает список строк, для настройки интерфейса.

Например:
```python
In [1]: config_interface('Fa0/1', '10.0.1.1', '/25')
Out[1]: ['interface Fa0/1', 'no shutdown', 'ip address 10.0.1.1 255.255.255.128']

In [2]: config_interface('Fa0/3', '10.0.0.1', '/18')
Out[2]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.192.0']

In [3]: config_interface('Fa0/3', '10.0.0.1', '/32')
Out[3]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.255.255']

In [4]: config_interface('Fa0/3', '10.0.0.1', '/30')
Out[4]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.255.252']

In [5]: config_interface('Fa0/3', '10.0.0.1', '30')
Out[5]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.255.252']
```

Но, что, если теперь не мы вручную вызываем функцию, а нам нужно вызывать её, передав на вход информацию, которую мы получили из другого источника.

Например, у нас есть список interfaces_info, в котором находятся параметры для настройки интерфейсов:
```python
In [6]: interfaces_info = [['Fa0/1', '10.0.1.1', '/24'],
   ....:                    ['Fa0/2', '10.0.2.1', '/24'],
   ....:                    ['Fa0/3', '10.0.3.1', '/24'],
   ....:                    ['Fa0/4', '10.0.4.1', '/24'],
   ....:                    ['Lo0', '10.0.0.1', '/32']]
```

Если мы теперь попробуем пройтись по списку в цикле, и просто передавать вложенный список, как аргумент, мы получим ошибку:
```
In [7]: for info in interfaces_info:
   ....:     print config_interface(info)
   ....:
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-32-fb83ecc1fbcf> in <module>()
      1 for info in interfaces_info:
----> 2     print config_interface(info)
      3

TypeError: config_interface() takes exactly 3 arguments (1 given)
``` 

Ошибка вполне логичная, наша функция ожидает три аргумента, а мы ей передаем 1 аргумент - список.

И вот в такой ситуации, очень пригодится распаковка аргументов.
Нам достаточно только добавить ```*``` перед передачей списка, как аргумента, и всё получится:```python
In [8]: for info in interfaces_info:
   ....:     print config_interface(*info)
   ....:
['interface Fa0/1', 'no shutdown', 'ip address 10.0.1.1 255.255.255.0']
['interface Fa0/2', 'no shutdown', 'ip address 10.0.2.1 255.255.255.0']
['interface Fa0/3', 'no shutdown', 'ip address 10.0.3.1 255.255.255.0']
['interface Fa0/4', 'no shutdown', 'ip address 10.0.4.1 255.255.255.0']
['interface Lo0', 'no shutdown', 'ip address 10.0.0.1 255.255.255.255']
```

Python сам 'распакует' список info и передаст в функцию элементы списка, как аргументы.

> Таким же образом можно распаковывать и кортеж.

### Распаковка ключевых аргументов

Аналогичным образом, можно распаковывать словарь, чтобы передать его как ключевые аргументы.

Например, у нас есть функция config_to_list:
```python
def config_to_list(cfg_file, delete_excl=True,
                   delete_empty=True, strip_end=True):
    result = []
    with open( cfg_file ) as f:
        for line in f:
            if strip_end:
                line = line.rstrip()
            if delete_empty and not line:
                pass
            elif delete_excl and line.startswith('!'):
                pass
            else:
                result.append(line)
    return result
```

Она берет файл с конфигурацией, убирает часть строк и возвращает остальные строки как список.

> Весь код функции можно вставить в ipython с помощью команды %cpaste.

Пример использования:
```python
In [9]: config_to_list('r1.txt')
Out[9]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

И у нас есть список словарей, в которых указано имя файла и все аргументы:
```python
In [10]: cfg = [dict(cfg_file='r1.txt', delete_excl=True, delete_empty=True, strip_end=True),
   ....:        dict(cfg_file='r2.txt', delete_excl=False, delete_empty=True, strip_end=True),   ....:        dict(cfg_file='r3.txt', delete_excl=True, delete_empty=False, strip_end=True),   ....:        dict(cfg_file='r4.txt', delete_excl=True, delete_empty=True, strip_end=False)]
```

Если мы будем передавать словарь функции config_to_list, то мы получим ошибку:
```python
In [11]: for d in cfg:
   ....:     print config_to_list(d)
   ....:
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-40-1affbd99c2f5> in <module>()
      1 for d in cfg:
----> 2     print config_to_list(d)
      3

<ipython-input-35-6337ba2bfe7a> in config_to_list(cfg_file, delete_excl, delete_empty, strip_end)
      2                    delete_empty=True, strip_end=True):
      3     result = []
----> 4     with open( cfg_file ) as f:
      5         for line in f:
      6             if strip_end:

TypeError: coercing to Unicode: need string or buffer, dict found
```

Ошибка такая, так как все параметры, кроме имени файла, опциональны.
И на стадии открытия файла, возникает ошибка, так как мы передали словарь.

Но, если мы добавим ```**``` перед передачей словаря функции, то функция нормально отработает:
```
In [12]: for d in cfg:
    ...:     print config_to_list(**d)
    ...:
['service timestamps debug datetime msec localtime show-timezone year', 'service timestamps log datetime msec localtime show-timezone year', 'service password-encryption', 'service sequence-numbers', 'no ip domain lookup', 'ip ssh version 2']
['!', 'service timestamps debug datetime msec localtime show-timezone year', 'service timestamps log datetime msec localtime show-timezone year', 'service password-encryption', 'service sequence-numbers', '!', 'no ip domain lookup', '!', 'ip ssh version 2', '!']
['service timestamps debug datetime msec localtime show-timezone year', 'service timestamps log datetime msec localtime show-timezone year', 'service password-encryption', 'service sequence-numbers', '', '', '', 'ip ssh version 2', '']
['service timestamps debug datetime msec localtime show-timezone year\n', 'service timestamps log datetime msec localtime show-timezone year\n', 'service password-encryption\n', 'service sequence-numbers\n', 'no ip domain lookup\n', 'ip ssh version 2\n']
```

Python распаковывает словарь и передает его в функцию как ключевые аргументы.


