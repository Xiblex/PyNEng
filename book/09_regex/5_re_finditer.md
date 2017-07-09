### ```re.finditer()```

Для того чтобы получить все совпадения, но при этом, получить совпадения в виде объекта Match(), можно использовать функцию ```finditer()```:
```python
In [23]: line2 = 'test dhcp, test2 dhcp2'

In [24]: match = re.finditer('dhcp', line2)

In [25]: print(match)
<callable-iterator object at 0x10efd2cd0>

In [26]: for i in match:
   ....:     print(i.span())
   ....:     
(5, 9)
(17, 21)

In [27]: line2[5:9]
Out[27]: 'dhcp'

In [28]: line2[17:21]
Out[28]: 'dhcp'
```

Можно воспользоваться и методами ```start()```, ```end()``` (так удобнее получить позиции подстрок):
```python
In [29]: line2 = 'test dhcp, test2 dhcp2'

In [30]: match = re.finditer('dhcp', line2)

In [31]: for i in match:
   ....:     b = i.start()
   ....:     e = i.end()
   ....:     print(line2[b:e])
   ....:     
dhcp
dhcp
```


