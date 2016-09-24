##Magic commands

В ipython есть "волшебные" команды.

Все они начинаются на %.

Например, команда __```%history```__ позволяет просмотреть историю текущей сессии:
```python
In [1]: a = 10

In [2]: b = 5

In [3]: if a > b:
   ...:     print "A is bigger"
   ...:
A is bigger

In [4]: %history
a = 10
b = 5
if a > b:
    print "A is bigger"
%history
```

Таким образом вы можете скопировать какой-то блок кода.

Еще одна очень полезная волшебная команда ```%cpaste```

Проблема в том, что когда вы вставляете блок кода в ipython, в котором есть отступы, из-за автоматических отступов самого ipython у вас начинает сдвигаться код:
```python
In [1]: a = 10

In [2]: b = 5

In [3]: if a > b:
   ...:     print "A is bigger"
   ...: else:
   ...:     print "A is less or equal"
   ...:
A is bigger

In [4]: %hist
a = 10
b = 5
if a > b:
    print "A is bigger"
else:
    print "A is less or equal"
%hist

In [5]: if a > b:
   ...:         print "A is bigger"
   ...:     else:
   ...:             print "A is less or equal"
   ...:
  File "<ipython-input-8-4d18ff094f5c>", line 3
    else:
         ^
IndentationError: unindent does not match any outer indentation level

If you want to paste code into IPython, try the %paste and %cpaste magic functions.
```

Обратите внимание на последнюю строку. iPython лапочка и говорит нам какой командой воспользоваться, чтобы корректно вставить такой код.


Магия %paste и %cpaste работает немного по-разному.

__%cpaste__ (после того как все строки скопированы, надо завершить работу команду набрав '--'):
```python
In [9]: %cpaste
Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
:if a > b:
:    print "A is bigger"
:else:
:    print "A is less or equal"
:--
A is bigger
```

__%paste__ (требует установленного Tkinter):
```python
In [10]: %paste
if a > b:
    print "A is bigger"
else:
    print "A is less or equal"

## -- End pasted text --
A is bigger
```