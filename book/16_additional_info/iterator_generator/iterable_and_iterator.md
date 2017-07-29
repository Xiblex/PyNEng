## Итераторы и итерируемые объекты

Итерация - это общий термин, который описывает процедуру взятия элементов чего-то по очереди.

В более общем смысле, это последовательность инструкций, которая повторяется определенное количество раз или до выполнения указанного условия.

### Итерируемый объект

Итерируемый объект (iterable) - это объект из которого можно получить итератор.

> Более простыми словами, итерируемый объект - это объект, который способен возвращать элементы по одному.

В Python за получение итератора отвечает функция iter():
```python
In [1]: lista = [1, 2, 3]

In [2]: iter(lista)
Out[2]: <list_iterator at 0xb4ede28c>
```

Функция iter() отработает на любом объекте у которого есть метод ```__iter__``` или метод ```__getitem__```.

Метод ```__iter__``` возвращает итератор.
Но, если этого метода нет, функция iter() проверяет нет ли метода ```__getitem__``` - метод, который позволяет получать элементы по индексу.

Если метод ```__getitem__``` есть, возвращается итератор, который проходится по элементам используя индекс (начиная с 0).

На практике, использование метода ```__getitem__``` означает, что все последовательности элементов - это итерируемые объекты. Например, список, кортеж, строка.
Хотя, у этих типов данных есть и метод ```__iter__```.

Примеры итерируемых объектов:
* все последовательности: list, str, tuple
* словари
* файлы

### Итератор

Итератор (iterator) - это объект, который возвращает свои элементы по одному за раз.

С точки зрения Python, это любой объект, у которого есть метод ```__next__```. Этот метод возвращает следующий элемент, если он есть или возвращает исключение StopIteration, когда элементы закончились.

Кроме того, итератор запоминает на каком объекте он остановился в последнюю итерацию.

В Python у каждого итератора присутствует метод ```__iter__``` - то есть, любой итератор является итерируемым объектом. Этот метод просто возвращает сам итератор.


Пример создания итератора из списка:
```python
In [3]: lista = [1, 2, 3]

In [4]: i = iter(lista)
```

Теперь можно использовать функцию next(), которая вызывает метод ```__next__```, чтобы взять следующий элемент:
```python
In [5]: next(i)
Out[5]: 1

In [6]: next(i)
Out[6]: 2

In [7]: next(i)
Out[7]: 3

In [8]: next(i)
------------------------------------------------------------
StopIteration              Traceback (most recent call last)
<ipython-input-8-bed2471d02c1> in <module>()
----> 1 next(i)

StopIteration:
```

После того как элементы закончились, возвращается исключение StopIteration.

> Для того чтобы итератор снова начал возвращать элементы, его надо заново создать.

Аналогичные действия выполяются, когда цикл for проходится по списку:
```python
In [9]: for item in lista:
   ...:     print(item)
   ...:
1
2
3

```

Когда мы перебираем элементы списка, к списку сначала применяется функция iter(), чтобы создать итератор, а затем вызывается его метод ```__next__``` до тех пор, пока не возникнет исключение StopIteration.

Конечно, когда итератор создается из списка или словаря, не до конца понятно зачем он вообще нужен, кроме предоставления возможности проходиться по элементам.

Кроме этого, итераторы полезны тем, что ни отдают элементы по одному.
Например, при работе с файлом, это полезно тем, что в памяти будет находиться не весь файл, а только одна строка файла.

### Файл как итератор

Один из самых распространенных примеров итератора - файл.

Файл r1.txt:
```
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
```

Если открыть файл обычной функцией open, мы получим объект, который представляет файл:
```python
In [10]: f = open('r1.txt')
```

Этот объект является итератором, что можно проверить вызвав метод ```__next__```:
```python
In [11]: f.__next__()
Out[11]: '!\n'

In [12]: f.__next__()
Out[12]: 'service timestamps debug datetime msec localtime show-timezone year\n'

```


Аналогичным образом можно перебирать строки в цикле for:
```python
In [13]: for line in f:
    ...:     print(line.rstrip())
    ...:
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
```

При работе с файлами, использование файла как итератора не просто позволяет перебирать файл построчно  в каждую итерацию загружена только одна строка.
Это очень важно при работе с большими файлами на тысячи и сотни тысяч строк.
Например, с лог-файлами.

Поэтому при работе с файлами, в Python, чаще всего, используется конструкция вида:
```python
In [14]: with open('r1.txt') as f:
    ...:     for line in f:
    ...:         print(line.rstrip())
    ...:
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
```

### enumerate

Иногда, при переборе объектов в цикле for, нужно не только получить сам объект, но и его порядковый номер.
Это можно сделать, создав дополнительную переменную, которая будет расти на единицу с каждым прохождением цикла.
Но, гораздо удобнее это делать с помощью итератора __```enumerate()```__.

Базовый пример:
```python
In [15]: list1 = ['str1', 'str2', 'str3']

In [16]: for position, string in enumerate(list1):
    ...:     print(position, string)
    ...:
0 str1
1 str2
2 str3
```

```enumerate()``` умеет считать не только с нуля, но и с любого значение, которое ему указали после объекта:
```python
In [17]: list1 = ['str1', 'str2', 'str3']

In [18]: for position, string in enumerate(list1, 100):
    ...:     print(position, string)
    ...:
100 str1
101 str2
102 str3
```

Иногда нужно проверить, что сгенерировал итератор, как правило, на стадии написания скрипта.
Если необходимо увидеть содержимое, которое сгенерирует итератор, полностью, можно воспользоваться функцией list:
```python
In [19]: list1 = ['str1', 'str2', 'str3']

In [20]: list(enumerate(list1, 100))
Out[20]: [(100, 'str1'), (101, 'str2'), (102, 'str3')]
```

#### Пример использования enumerate для EEM

В этом примере используется Cisco [EEM](http://xgu.ru/wiki/EEM).
Если в двух словах, то EEM позволяет выполнять какие-то действия (action) в ответ на событие (event).

Выглядит applet EEM так:
```python
event manager applet Fa0/1_no_shut
 event syslog pattern "Line protocol on Interface FastEthernet0/0, changed state to down"
 action 1 cli command "enable"
 action 2 cli command "conf t"
 action 3 cli command "interface fa0/1"
 action 4 cli command "no sh"
```

В EEM, в ситуации, когда действий выполнить нужно много, неудобно каждый раз набирать ```action x cli command```.
Плюс, чаще всего, уже есть готовый кусок конфигурации, который должен выполнить EEM.

С помощью простого скрипта Python, можно сгенерировать команды EEM, на основании существующего списка команд (файл enumerate_eem.py):
```python
import sys

config = sys.argv[1]

with open(config, 'r') as file:
    for (i, command) in enumerate(file, 1):
        print('action {:04} cli command "{}"'.format( i, command.rstrip() ))

```

В данном примере команды считываются из файла, а затем к каждой строке добавляется приставка, которая нужна для EEM.

Файл с командами выглядит так (r1_config.txt):
```python
en
conf t
no int Gi0/0/0.300
no int Gi0/0/0.301
no int Gi0/0/0.302
int range gi0/0/0-2
 channel-group 1 mode active
interface Port-channel1.300
 encapsulation dot1Q 300
 vrf forwarding Management
 ip address 10.16.19.35 255.255.255.248
```

Вывод будет таким:
```python
$ python enumerate_eem.py r1_config.txt
action 0001 cli command "en"
action 0002 cli command "conf t"
action 0003 cli command "no int Gi0/0/0.300"
action 0004 cli command "no int Gi0/0/0.301"
action 0005 cli command "no int Gi0/0/0.302"
action 0006 cli command "int range gi0/0/0-2"
action 0007 cli command " channel-group 1 mode active"
action 0008 cli command "interface Port-channel1.300"
action 0009 cli command " encapsulation dot1Q 300"
action 0010 cli command " vrf forwarding Management"
action 0011 cli command " ip address 10.16.19.35 255.255.255.248"
```

