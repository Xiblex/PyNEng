## Интерпретатор Python. iPython

Интерпретатор позволяет получать моментальный отклик на выполненные действия.

Можно сказать, что интерпретатор работает как командная строка сетевых устройств: каждая команда будет выполняться сразу после нажатия enter (по крайней мере, похоже на cisco).

Но для интерпретатора Python есть исключение: более сложные объекты (например, циклы, функции) выполняются только после нажатия enter два раза.

В предыдущем разделе для проверки установки Python вызвался стандартный интерпретатор.

Но, кроме него, в Python есть усовершенствованный интерпретатор iPython ([документация iPython](http://ipython.readthedocs.io/en/stable/index.html)).

iPython позволяет намного больше, чем стандартный интерпретатор, который вызывается по команде python.

Несколько примеров (возможности ipython намного шире):
* автопродолжение команд по Tab или подсказка, если вариантов команд несколько
* более структурированный и понятный вывод команд
* автоматические отступы в циклах и других объектах
* история выполнения команд
  * по ней можно передвигаться
  * или посмотреть "волшебной" командой %history

Установить iPython можно с помощью pip (установка в виртуальном окружении):
```
pip install ipython
```

__Далее как интерпретатор будет использоваться iPython.__


Для знакомства с интерпретатором можно попробовать его использовать как калькулятор:
```python
In [1]: 1 + 2
Out[1]: 3

In [2]: 22*45
Out[2]: 990

In [3]: 2**3
Out[3]: 8
```

В iPython ввод и вывод подписаны:
* In - это то, что написал пользователь
* Out - это вывод команды (если он есть)
* Числа после In и Out - это нумерация выполненных команд в текущей сессии iPython
 
Пример вывода строки:
```python
In [4]: print('Hello!')
Hello!
```

Когда в интерпретаторе создается, например, цикл, то внутри цикла приглашение меняется на ```...```.
Для выполнения цикла и выхода из этого подрежима необходимо дважды нажать Enter:
```python
In [5]: for i in range(5):
   ...:     print(i)
   ...:     
0
1
2
3
4
```

### help

В ipython есть возможность посмотреть help по какому-то объекту, функции или методу:
```python
In [1]: help(str)
Help on class str in module builtins:
 
class str(object)
 |  str(object='') -> str
 |  str(bytes_or_buffer[, encoding[, errors]]) -> str
 |
 |  Create a new string object from the given object. If encoding or
 |  errors is specified, then the object must expose a data buffer
 |  that will be decoded using the given encoding and error handler.
...
 
In [2]: help(str.strip)
Help on method_descriptor:
 
strip(...)
    S.strip([chars]) -> str
 
    Return a copy of the string S with leading and trailing
    whitespace removed.
    If chars is given and not None, remove characters in chars instead.
```

Второй вариант:
```python
In [3]: ?str
Init signature: str(self, /, *args, **kwargs)
Docstring:
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str
 
Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
Type:           type
 
In [4]: ?str.strip
Docstring:
S.strip([chars]) -> str
 
Return a copy of the string S with leading and trailing
whitespace removed.
If chars is given and not None, remove characters in chars instead.
Type:      method_descriptor
```

### print

Функция print позволяет вывести информацию на стандартный поток вывода.

Если необходимо вывести строку, то ее нужно обязательно заключить в кавычки (двойные или одинарные). Если же нужно вывести, например, результат вычисления или просто число, то кавычки не нужны:
```python
In [6]: print('Hello!')
Hello!

In [7]: print(5*5)
25
```

Если нужно вывести несколько значений, можно перечислить их через запятую:
```python
In [8]: print(1*5, 2*5, 3*5, 4*5)
5 10 15 20

In [9]: print('one', 'two', 'three')
one two three
```
 
> Подробнее о [функции print](../07_functions/useful_functions/print.md)

По умолчанию в конце выражения будет перевод строки.
Если необходимо, чтобы после вывода выражения не было перевода строки, надо указать дополнительный аргумент ```end```.

По умолчанию он равен ```\n```, поэтому к строке или строкам в print добавляется перевод строки.

Например, такое выражение выведет строки 'one' и 'two' в разных строках:
```python
In [10]: print('one'), print('two')
one
two
Out[10]: (None, None)
```

Но если в первой функции print указать параметр end равным пустой строке, результат будет таким:
```python
In [11]: print('one', end=''), print('two')
onetwo
Out[11]: (None, None)
```

### dir
Команда dir() может использоваться для того, чтобы посмотреть, какие атрибуты и методы есть у объекта.

Например, для числа вывод будет таким (обратите внимание на различные методы, которые позволяют делать арифметические операции):
```python
In [10]: dir(5)
Out[10]: 
['__abs__',
 '__add__',
 '__and__',
 ...
 'bit_length',
 'conjugate',
 'denominator',
 'imag',
 'numerator',
 'real']
```

Для строки:
```python
In [11]: dir('hello')
Out[11]: 
['__add__',
 '__class__',
 '__contains__',
 ...
 'startswith',
 'strip',
 'swapcase',
 'title',
 'translate',
 'upper',
 'zfill']
```

Если выполнить команду без передачи значения, то она показывает существующие методы, атрибуты и переменные, определенные в текущей сессии интерпретатора:
```python
In [12]: dir()
Out[12]: 
[ '__builtin__',
 '__builtins__',
 '__doc__',
 '__name__',
 '_dh',
 ...
 '_oh',
 '_sh',
 'exit',
 'get_ipython',
 'i',
 'quit']
```

Пример после создания переменной __a__ и функции __test__:
```python
In [13]: a = 'hello'

In [14]: def test():
   ....:     print('test')
   ....:     

In [15]: dir()
Out[15]: 
 ...
 'a',
 'exit',
 'get_ipython',
 'i',
 'quit',
 'test']
```

