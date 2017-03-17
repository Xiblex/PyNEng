## Импорт модуля

В Python есть несколько способов импорта модуля:
* ```import module```
* ```import module as```
* ```from module import object```
* ```from module import *```


### ```import module```

Вариант __import module__:
```python
In [1]: dir()
Out[1]: 
['In',
 'Out',
 ...
 'exit',
 'get_ipython',
 'quit']

In [2]: import os

In [3]: dir()
Out[3]: 
['In',
 'Out',
 ...
 'exit',
 'get_ipython',
 'os',
 'quit']
```

После импорта, модуль os появился в выводе dir(). Это значит, что он теперь в текущем именном пространстве.

Чтобы вызвать какую-то функцию или метод из модуля os, надо указать ```os.``` и затем имя объекта:
```python
In [4]: os.getlogin()
Out[4]: 'natasha'
```

Этот способ импорта хорош тем, что объекты модуля не попадают в именное пространство текущей программы.
То есть, если создать функцию с именем getlogin(), она не будет конфликтовать с аналогичной функцией модуля os.

> Если в имени файла содержится точка, стандартный способ импортирования не будет работать.
> Для таких случаев, используется [другой способ](http://stackoverflow.com/questions/1828127/how-to-reference-python-package-when-filename-contains-a-period/1828249#1828249).


### ```import module as```

Конструкция __import module as__ позволяет импортировать модуль под другим именем (как правило, более коротким):
```python
In [1]: import subprocess as sp

In [2]: sp.check_output('ping -c 2 -n  8.8.8.8', shell=True)
Out[2]: 'PING 8.8.8.8 (8.8.8.8): 56 data bytes\n64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.880 ms\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=46.875 ms\n\n--- 8.8.8.8 ping statistics ---\n2 packets transmitted, 2 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 46.875/48.377/49.880/1.503 ms\n'
```


### ```from module import object```
Вариант __from module import object__ удобно использовать, когда из всего модуля нужны только одна-две функции:

```python
In [1]: from os import getlogin, getcwd
```

Теперь эти функции доступны в текущем именном пространстве:
```python
In [2]: dir()
Out[2]: 
['In',
 'Out',
 ...
 'exit',
 'get_ipython',
 'getcwd',
 'getlogin',
 'quit']
```

Их можно вызывать без имени модуля:
```python
In [3]: getlogin()
Out[3]: 'natasha'

In [4]: getcwd()
Out[4]: '/Users/natasha/Desktop/Py_net_eng/code_test'
```

### ```from module import *```

Вариант __from module import *__ импортирует все имена модуля в текущее именное пространство:
```python
In [1]: from os import *

In [2]: dir()
Out[2]: 
['EX_CANTCREAT',
 'EX_CONFIG',
 ...
 'wait',
 'wait3',
 'wait4',
 'waitpid',
 'walk',
 'write']

In [3]: len(dir())
Out[3]: 218
```

В модуле os очень много объектов, поэтому вывод сокращен. В конце указана длина списка имен текущего именного пространства.

Такой вариант импорта лучше не использовать.
При таком импорте, по коду не понятно, что какая-то функция взята из модуля os, например.
Это заметно усложняет понимание кода.


