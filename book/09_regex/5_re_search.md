### ```re.search()```

Функция ```search()```:
* используется для поиска подстроки, которая соответствует шаблону
* возвращает объект Match, если подстрока найдена
* возвращает ```None```, если подстрока не найдена


Поиск подстроки в строке:
```python
In [1]: import re

In [2]: line = '00:09:BB:3D:D6:58   10.1.10.2    86250   dhcp-snooping   10    FastEthernet0/1'

In [3]: print(re.search('dhcp', line))
<_sre.SRE_Match object; span=(41, 45), match='dhcp'>

In [4]: print(re.search('dhcpd', line))
None
```


Из объекта Match можно получить несколько вариантов полезной информации.

Например, с помощью метода ```span()```, можно получить числа, указывающие начало и конец подстроки: 
```python
In [5]: match = re.search('dhcp', line)

In [6]: match.span()
Out[6]: (41, 45)

In [7]: line[41:45]
Out[7]: 'dhcp'
```

Метод ```group()``` позволяет получить подстроку, которая соответствует шаблону:
```python
In [15]: match.group()
Out[15]: 'dhcp'
```

Важный момент в использовании функции ```search()```, то что она ищет только первое совпадение в строке, которое соответствует шаблону:
```python
In [16]: line2 = 'test dhcp, test2 dhcp2'

In [17]: match = re.search('dhcp', line2)

In [18]: match.group()
Out[18]: 'dhcp'

In [19]: match.span()
Out[19]: (5, 9)
```

