## Ввод информации пользователем

Иногда, необходимо получить информацию от пользователя.
Попробуем сделать так, чтобы скрипт задавал вопросы пользователю и затем использовал этот ответ.

> Ввод от пользователя может понадобиться, например, для того, чтобы ввести пароль.

Для получения информации от пользователя используется функция raw_input():
```python
In [1]: print raw_input('Твой любимый протокол маршрутизации? ')
Твой любимый протокол маршрутизации? OSPF
OSPF
```

В данном случае, информация просто тут же выводится пользователю, но кроме этого, информация, которую ввел пользователь может быть сохранена в какую-то переменную.
И может использоваться далее в скрипте.
```python
In [2]: protocol = raw_input('Твой любимый протокол маршрутизации? ')
Твой любимый протокол маршрутизации? OSPF

In [3]: print protocol
OSPF
```

В скобках обычно пишется какой-то вопрос, который уточняет, какую информацию нужно ввести.

Текст в скобках, в принципе, писать не обязательно.
И можно сделать такой же вывод с помощью оператора __print__::
```python
In [4]: print 'Твой любимый протокол маршрутизации?'
Твой любимый протокол маршрутизации?

In [5]: protocol = raw_input()
OSPF

In [6]: print protocol
OSPF
```

Но, как правило, нагляднее писать текст в самой функции raw_print().

Запрашивание информации из скрипта (файл access_template_raw_input.py):
```python

interface = raw_input('Enter interface type and number: ')
vlan = int(raw_input('Enter VLAN number: '))

access_template = ['switchport mode access',
                   'switchport access vlan %d',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

print '\n' + '-' * 30
print 'interface %s' % interface
print '\n'.join(access_template) % vlan
```

В первых двух строках, запрашивается информация у пользователя.
Функция raw_input(), как и argv возвращает данные в виде строк.
Поэтому, параметр vlan преобразуем в число.

Еще появилась строка ```print '\n' + '-' * 30```.
Она используется просто для того, чтобы отделить запрос информации от вывода.

Выполняем скрипт:
```
$ python access_template_raw_input.py
Enter interface type and number: Gi0/3
Enter VLAN number: 55

------------------------------
interface Gi0/3
switchport mode access
switchport access vlan 55
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
```

> Если Вы знаете о том, что существует еще функция ```input()``` и запутались какая разница между __raw_input()__ и __input()__, посмотрите эту ссылку:
http://stackoverflow.com/questions/4915361/whats-the-difference-between-raw-input-and-input-in-python3-x

