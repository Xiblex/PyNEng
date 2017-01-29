### Полезные методы для работы со словарями

####```clear()```

Метод __clear()__ позволяет очистить словарь:
```python
In [1]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco', 'model': '4451', 'IOS': '15.4'}

In [2]: london.clear()

In [3]: london
Out[3]: {}
```

####```copy()```

Метод __copy()__ позволяет создать полную копию словаря. 

Если указать, что один словарь равен другому:
```python
In [4]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [5]: london2 = london

In [6]: id(london)
Out[6]: 25489072

In [7]: id(london2)
Out[7]: 25489072

In [8]: london['vendor'] = 'Juniper'

In [9]: london2['vendor']
Out[9]: 'Juniper'
```

В этом случае london2 это еще одно имя, которое ссылается на словарь.
И, при изменениях словаря london, меняется и словарь london2, так как это ссылки на один и тот же объект.

Поэтому, если нужно сделать копию словаря, надо использовать метод copy():
```python
In [10]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [11]: london2 = london.copy()

In [12]: id(london)
Out[12]: 25524512

In [13]: id(london2)
Out[13]: 25563296

In [14]: london['vendor'] = 'Juniper'

In [15]: london2['vendor']
Out[15]: 'Cisco'
```

####```get()```

Если при обращении к словарю указывается ключ, которого нет в словаре, возникает ошибка:
```python
In [16]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [17]: london['IOS']
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-17-b4fae8480b21> in <module>()
----> 1 london['IOS']

KeyError: 'IOS'
```

Метод __get()__ запрашивает ключ и, если его нет, вместо ошибки возвращает ```None```.
```python
In [18]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [19]: print london.get('IOS')
None
```

Метод get() позволяет указывать другое значение, вместо ```None```:
```python
In [20]: print london.get('IOS', 'Ooops')
Ooops
```

####```keys(), values(), items()```

Методы __keys()__, __values()__, __items()__:
```python
In [24]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [25]: london.keys()
Out[25]: ['vendor', 'name', 'location']

In [26]: london.values()
Out[26]: ['Cisco', 'London1', 'London Str']

In [27]: london.items()
Out[27]: [('vendor', 'Cisco'), ('name', 'London1'), ('location', 'London Str')]
```

####```del```
Удалить ключ и значение:
```python
In [28]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [29]: del(london['name'])

In [30]: london
Out[30]: {'location': 'London Str', 'vendor': 'Cisco'}
```
