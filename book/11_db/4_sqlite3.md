## Модуль sqlite3
Для работы с SQLite в Python используется модуль sqlite3.


### Connection

Объект __Connection__ - это подключение к конкретной БД. Можно сказать, что этот объект представляет БД.

Пример создания подключения:
```python
import sqlite3

connection = sqlite3.connect('dhcp_snooping.db')
```

### Cursor

После создания соединения, надо создать объект Cursor - это основной способ работы с БД.

Создается курсор из соединения с БД:
```python
connection = sqlite3.connect('dhcp_snooping.db')
cursor = connection.cursor()
```

### Выполнение команд SQL

Для выполнения команд SQL в модуле есть несколько методов:
* __```execute()```__ - метод для выполнения одного выражения SQL
* __```executemany()```__ - метод позволяет выполнить одно выражение SQL для последовательности параметров (или для итератора)
* __```executescript()```__ - метод позволяет выполнить несколько выражений SQL за один раз


#### Метод execute

Метод execute позволяет выполнить одну команду SQL.


Сначала надо создать соединение и курсор:
```python
In [1]: import sqlite3

In [2]: connection = sqlite3.connect('sw_inventory.db')

In [3]: cursor = connection.cursor()
```

Создание таблицы switch с помощью метода execute:
```python
In [4]: cursor.execute("create table switch (mac text primary key, hostname text, model text, location text)")
Out[4]: <sqlite3.Cursor at 0x1085be880>
```

Выражения SQL могут быть параметризированы - вместо данных можно подставлять специальные значения.
Засчет этого можно использовать одну и ту же команду SQL для передачи разных данных.


Например, таблицу switch нужно заполнить данными из списка data:
```python
In [5]: data = [
   ...: ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
   ...: ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
   ...: ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]
```

Для этого можно использовать запрос вида:
```python
In [6]: query = "INSERT into switch values (?, ?, ?, ?)"
```

Знаки вопроса в команде используются для подстановки данных, которые будут передаваться методу execute.

Теперь можно передать данные таким образом:
```
In [7]: for row in data:
   ...:     cursor.execute(query, row)
   ...:
```

Второй аргумент, который передается методу execute, должен быть кортежем.
Если нужно передать кортеж с одним элементом, используется запись ```(value, )```.

Чтобы изменения применились, нужно выполнить commit (обратите внимание, что метод commit вызывается у соединения):
```
In [8]: connection.commit()
```

Теперь, при запросе из командной строки sqlite3, можно увидеть эти строки в таблице switch:
```
$ sqlite3 sw_inventory.db

sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3780  London, Green Str
0000.AAAA.DDDD  sw3         Cisco 2960  London, Green Str
0011.AAAA.CCCC  sw4         Cisco 3750  London, Green Str
```

#### Метод executemany

Метод executemany позволяет выполнить одну команду SQL для последовательности параметров (или для итератора).

С помощью метода executemany, в таблицу switch можно добавить аналогичный список данных одной командой.

Например, в таблицу switch надо добавить данные из списка data2:
```python
In [9]: data2 = [
   ...: ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]
```

Для этого нужно использовать аналогичный запрос вида:
```python
In [10]: query = "INSERT into switch values (?, ?, ?, ?)"
```

Теперь можно передать данные методу executemany:
```python
In [11]: cursor.executemany(query, data2)
Out[11]: <sqlite3.Cursor at 0x10ee5e810>

In [12]: connection.commit()
```

После выполнения commit, данные доступны в таблице:
```
sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3780  London, Green Str
0000.AAAA.DDDD  sw3         Cisco 2960  London, Green Str
0011.AAAA.CCCC  sw4         Cisco 3750  London, Green Str
0000.1111.0001  sw5         Cisco 3750  London, Green Str
0000.1111.0002  sw6         Cisco 3750  London, Green Str
0000.1111.0003  sw7         Cisco 3750  London, Green Str
0000.1111.0004  sw8         Cisco 3750  London, Green Str
```

Метод executemany подставил соответствующие кортежи в команду SQL и все данные добавились в таблицу.


#### Метод executescript

Метод executescript позволяет выполнить несколько выражений SQL за один раз.


Особенно удобно использовать этот метод при создании таблиц:
```python
In [14]: connection = sqlite3.connect('new_db.db')

In [15]: cursor = connection.cursor()

In [16]: cursor.executescript("""
    ...:     create table switches(
    ...:         hostname     text primary key,
    ...:         location     text
    ...:     );
    ...:
    ...:     create table dhcp(
    ...:         mac          text primary key,
    ...:         ip           text,
    ...:         vlan         text,
    ...:         interface    text,
    ...:         switch       text not null references switches(hostname)
    ...:     );
    ...: """)
Out[16]: <sqlite3.Cursor at 0x10efd67a0>
```

### Получение результатов запроса

Для получения результатов запроса в sqlite3 есть несколько способов:
* использование методов ```fetch...()``` - в зависимости от метода возвращаются одна, несколько или все строки
* использование курсора как итератора - возвращается итератор

#### Метод fetchone

Метод fetchone возвращает одну строку данных.

Пример получения информации из базы данных sw_inventory.db:
```python
In [1]: import sqlite3

In [2]: connection = sqlite3.connect('sw_inventory.db')

In [3]: cursor = connection.cursor()

In [4]: cursor.execute('select * from switch')
Out[4]: <sqlite3.Cursor at 0x104eda810>

In [5]: cursor.fetchone()
Out[5]: (u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
```

Обратите внимание, что хотя запрос SQL подразумевает, что запрашивалось всё содержимое таблицы, метод fetchone вернул только одну строку.

Если повторно вызвать метод, он вернет следующую строку:
```python
In [6]: print cursor.fetchone()
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
```

Аналогичным образом метод будет возвращать следующие строки.
После обработки всех строк, метод начинает возвращать None.

Засчет этого, метод можно использовать в цикле, например, так:
```python
In [7]: cursor.execute('select * from switch')
Out[7]: <sqlite3.Cursor at 0x104eda810>

In [8]: while True:
   ...:     next_row = cursor.fetchone()
   ...:     if next_row:
   ...:         print next_row
   ...:     else:
   ...:         break
   ...:
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')
```

#### Метод fetchmany

Метод fetchmany возвращает возвращает список строк данных.

Синтаксис метода:
```
cursor.fetchmany([size=cursor.arraysize])
```

С помощью параметра size, можно указывать какое количество строк возвращается.
По умолчанию, параметр size равен значению cursor.arraysize:
```python
In [9]: print cursor.arraysize
1
```

Например, таким образом можно возвращать по три строки из запроса:
```python

In [10]: cursor.execute('select * from switch')
Out[10]: <sqlite3.Cursor at 0x104eda810>

In [11]: while True:
    ...:     three_rows = cursor.fetchmany(3)
    ...:     if three_rows:
    ...:         print three_rows
    ...:         print
    ...:     else:
    ...:         break
    ...:
[(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str'),
 (u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
 (u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')]

[(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str')]

[(u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')]
```

Метод выдает нужное количество строк, а если строк осталось меньше чем параметр size, то оставшиеся строки.

#### Метод fetchall

Метод fetchall возвращает все строки в виде списка:
```python
In [12]: cursor.execute('select * from switch')
Out[12]: <sqlite3.Cursor at 0x104eda810>

In [13]: cursor.fetchall()
Out[13]:
[(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str'),
 (u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str'),
 (u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str'),
 (u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')]
```

Важный аспект работы метода - он возвращает все оставшиеся строки.

То есть, если до метода fetchall, использовался, например, метод fetchone, то метод fetchall вернет оставшиеся строки запроса:
```python
In [14]: cursor.execute('select * from switch')
Out[14]: <sqlite3.Cursor at 0x104eda810>

In [15]: cursor.fetchone()
Out[15]: (u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')

In [16]: cursor.fetchone()
Out[16]: (u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')

In [17]: cursor.fetchall()
Out[17]:
[(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str'),
 (u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')]
```

Метод fetchmany, в этом аспекте, работает аналогично.

#### Cursor как итератор

Если нужно построчно обрабатывать результирующие строки, лучше использовать курсор как итератор.
При этом не нужно использовать методы fetch.

При использовании методов execute, возвращается курсор.
А, так как курсор можно использовать как итератор, можно использовать его, например, в цикле for:
```python
In [18]: result = cursor.execute('select * from switch')

In [19]: for row in result:
    ...:     print row
    ...:
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')
```


И, конечно же, аналогичный вариант отработает и без присваивания переменной:
```python
In [20]: for row in cursor.execute('select * from switch'):
    ...:     print row
    ...:
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')
```

### Использование модуля sqlite3

#### Без явного создания курсора

Методы execute доступны и в объекте Connection.
При их использовании курсор создается, но не явно.
Однако, методы fetch в Connection недоступны.

Но, если использовать курсор, который возвращают методы execute, как итератор, методы fetch могут и не понадобиться.


Пример итогового скрипта (файл create_sw_inventory_ver1.py):
```python
# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

con = sqlite3.connect('sw_inventory2.db')

con.execute("create table switch (mac text primary key, hostname text, model text, location text)")

query = "INSERT into switch values (?, ?, ?, ?)"
con.executemany(query, data)
con.commit()

for row in con.execute("select * from switch"):
    print row

con.close()
```

Результат выполнения будет таким:
```
$ python2 create_sw_inventory_ver1.py
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
```

#### Обработка исключений

Посмотрим на пример использования метода execute, при возникновении ошибки.


В таблице switch поле mac должно быть уникальным.
И, если попытаться записать пересекающийся MAC-адрес, возникнет ошибка:
```python
In [22]: con = sqlite3.connect('sw_inventory2.db')

In [23]: query = "INSERT into switch values ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str')"

In [24]: con.execute(query)
---------------------------------------------------------------------------
IntegrityError                            Traceback (most recent call last)
<ipython-input-56-ad34d83a8a84> in <module>()
----> 1 con.execute(query)

IntegrityError: UNIQUE constraint failed: switch.mac
```

Соответственно, можно перехватить исключение:
```python
In [25]: try:
    ...:     con.execute(query)
    ...: except sqlite3.IntegrityError as e:
    ...:     print "Error occured: ", e
    ...:
Error occured:  UNIQUE constraint failed: switch.mac
```

Обратите внимение, что надо перехватывать исключение sqlite3.IntegrityError, а не IntegrityError.


### Connection как менеджер контекста

После выполнения операций, изменения должны быть сохранены (надо выполнить ```commit()```), а затем можно закрыть соединение, если оно больше не нужно.

Python позволяет использовать объект Connection, как менеджер контекста.
В таком случае, не нужно явно делать commit и закрывать соединение.
При этом:
* при возникновении исключения, транзакция автоматически откатывается
* если исключения не было, автоматически выполняется commit

Пример использования соединения с базой, как менеджера контекстов (create_sw_inventory_ver2.py): 
```python
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

with sqlite3.connect('sw_inventory3.db') as con:

    con.execute("create table switch (mac text primary key, hostname text, model text, location text)")

    query = "INSERT into switch values (?, ?, ?, ?)"
    con.executemany(query, data)

    for row in con.execute("select * from switch"):
        print row
```

