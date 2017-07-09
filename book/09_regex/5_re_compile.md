### ```re.compile()```

В Python есть возможность заранее скомпилировать регулярное выражение, а затем использовать его. Это особенно полезно в тех случаях, когда регулярное выражение много используется в скрипте.

Пример компиляции регулярного выражения и его использования:
```python
In [32]: line2 = 'test dhcp, test2 dhcp2'

In [33]: regex = re.compile('dhcp')

In [34]: match = regex.finditer(line2)

In [35]: for i in match:
   ....:     b = i.start()
   ....:     e = i.end()
   ....:     print(line2[b:e])
   ....:     
dhcp
dhcp
```

