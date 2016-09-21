### Полезные методы для работы со словарями
Метод __clear()__ позволяет очистить словарь:
```python
In [1]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco', 'model': '4451', 'IOS': '15.4'}

In [2]: london.clear()

In [3]: london
Out[3]: {}
```

Метод __copy()__ позволяет создать полную копию словаря. 

Для начала проверим что будет есть сделать так:
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

В таком случае london2 это всего лишь еще одно имя, которое ссылается на словарь. И когда мы меняем словарь london, так как london2 по сути это тот же объект, получаем изменный словарь london2.

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

Метод __get()__.

Если при обращении к словарю указывается ключ, которого нет в словаре, мы получаем ошибку:
```python
In [16]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [17]: london['IOS']
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-17-b4fae8480b21> in <module>()
----> 1 london['IOS']

KeyError: 'IOS'
```

Метод __get()__ позволяет запросить значение, но если его нет, вместо ошибки возвращается указанное значение (по умолчанию возвращается None):
```python
In [18]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [19]: print london.get('IOS')
None

In [20]: print london.get('IOS', 'Ooops')
Ooops
```

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

Удалить ключ и значение:
```python
In [28]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [29]: del(london['name'])

In [30]: london
Out[30]: {'location': 'London Str', 'vendor': 'Cisco'}
```
