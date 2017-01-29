## Импорт модуля

Есть несколько способов импорта модуля:
* ```import module```
* ```import module as```
* ```from module import object```
* ```from module import *```

Попробуем в iPython проверить все варианты.

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

После импорта модуля os, он появился в выводе dir(), то есть, в нашем именном пространстве.
Если мы хотим использовать какой-то объект из модуля os, мы вызываем его так:
```python
In [4]: os.getlogin()
Out[4]: 'natasha'
```

То есть, мы должны указать имя модуля, а затем через точку метод, функцию или другой объект.

Этот способ импорта хорош тем, что объекты модуля не попадают в именное пространство текущей программы.
То есть, если мы создадим функцию с именем getlogin(), то мы не перебьем аналогичную функцию модуля os.

> Если в имени модуля содержится точка, стандартным способом модуль не получится импортировать.
> Для таких случаев, используется [другой способ](http://stackoverflow.com/questions/1828127/how-to-reference-python-package-when-filename-contains-a-period/1828249#1828249).


### ```import module as```

Конструкция __import module as__ позволяет импортировать модуль под другим именем (как правило, более коротким):
```python
In [1]: import sys as s

In [2]: s.path
Out[2]: 
['',
 '/usr/local/bin',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python27.zip',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-old',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC',
 '/Library/Python/2.7/site-packages',
 '/Library/Python/2.7/site-packages/IPython/extensions',
 '/Users/natasha/.ipython']
```


### ```from module import object```
Вариант __from module import object__ удобно использовать, когда из всего модуля нужны только одна-две функции:

```python
In [1]: from os import getlogin, getcwd
```

Теперь эти функции доступны в нашем именном пространстве:
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

Попробуем их использовать:
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

Но, такой вариант импорта, лучше не использовать.
Так как, при таком импорте, вы не поймете по коду, что какая-то функция взята из модуля os, например.
Это заметно усложняет понимание кода.


