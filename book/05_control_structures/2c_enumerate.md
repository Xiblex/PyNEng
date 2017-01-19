### Итератор enumerate()

Иногда, при переборе объектов в цикле for, нужно не только получить сам объект, но и его порядковый номер. Это можно сделать, создав дополнительную переменную, которая будет расти на единицу с каждым прохождением цикла.

Но, гораздо удобнее это делать с помощью итератора __enumerate()__.

Базовый пример:
```python
In [1]: list1 = ['str1', 'str2', 'str3']

In [2]: for position, string in enumerate(list1):
   ...:     print position, string
   ...:     
0 str1
1 str2
2 str3
```

enumerate() умеет считать не только с нуля, но и с любого значение, которое ему указали после объекта:
```python
In [1]: list1 = ['str1', 'str2', 'str3']

In [2]: for position, string in enumerate(list1, 100):
   ...:     print position, string
   ...:     
100 str1
101 str2
102 str3
```

#### Пример использования enumerate для EEM (advanced)

> Слово 'advanced' в заголовке, означает, что то, что рассматривается в этом разделе ещё не было в темах курса. Но, в дальнейшем, вам может пригодится такой прием.

Вероятно, вы знаете о такой вещи в Cisco, как [EEM](http://xgu.ru/wiki/EEM). Если в двух словах, то EEM позволяет выполнять какие-то действия (action) в ответ на событие (event).

Выглядит applet EEM так (подробнее в статье [EEM](http://xgu.ru/wiki/EEM)):
```python
event manager applet Fa0/1_no_shut
 event syslog pattern "Line protocol on Interface FastEthernet0/0, changed state to down"
 action 1 cli command "enable"
 action 2 cli command "conf t"
 action 3 cli command "interface fa0/1"
 action 4 cli command "no sh"
```

В EEM, в ситуации, когда действий выполнить нужно много, довольно быстро надоедает набирать ''action x cli command''. Плюс, чаще всего, уже есть готовый кусок конфигурации, который должен выполнить EEM.

Посмотрим как можно с помощью скрипта сгенерировать команды EEM, на основании существующего списка команд (файл eem.py):
```python
import sys

config = sys.argv[1]

with open(config, 'r') as file:
    for (i, command) in enumerate(file, 1):
        print 'action %04d cli command "%s"' % (i, command.rstrip())
```

В данном примере команды считываются из файла (конструкцию with и как работать с файлами мы рассмотрим позже), а затем мы обрабатываем каждую строку и добавляем к ней приставку, которая нужна для EEM.

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
$ python eem.py r1_config.txt
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

Упростим, и уберем считывание файла, чтобы было проще понять.

Теперь команды хранятся в списке:
```python 
In [1]: list1 = ['en\n',
   ...:  'conf t\n',
   ...:  'no int Gi0/0/0.300 \n',
   ...:  'no int Gi0/0/0.301 \n',
   ...:  'no int Gi0/0/0.302 \n',
   ...:  'int range gi0/0/0-2\n',
   ...:  ' channel-group 1 mode active\n',
   ...:  'interface Port-channel1.300\n',
   ...:  ' encapsulation dot1Q 300\n',
   ...:  ' vrf forwarding Management\n',
   ...:  ' ip address 10.16.19.35 255.255.255.248\n']
```

Повторяем цикл из файла:
```python
In [2]: for (i, command) in enumerate(list1, 1):
   ...:     print 'action %04d cli command "%s"' % (i, command.rstrip())
   ...:     
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

