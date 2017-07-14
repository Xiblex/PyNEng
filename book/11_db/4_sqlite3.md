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
In [13]: connection = sqlite3.connect('new_db.db')

In [14]: cursor = connection.cursor()

In [15]: cursor.executescript("""
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
Out[15]: <sqlite3.Cursor at 0x10efd67a0>
```

### Получение результатов запроса

Для получения результатов запроса в sqlite3 есть несколько способов:
* использование методов ```fetch...()``` - в зависимости от метода возвращаются одна, несколько или все строки
* использование курсора как итератора - возвращается итератор

#### Метод fetchone

Метод fetchone возвращает одну строку данных.

Пример получения информации из базы данных sw_inventory.db:
```python
In [16]: import sqlite3

In [17]: connection = sqlite3.connect('sw_inventory.db')

In [18]: cursor = connection.cursor()

In [19]: cursor.execute('select * from switch')
Out[19]: <sqlite3.Cursor at 0x104eda810>

In [20]: cursor.fetchone()
Out[20]: ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
```

Обратите внимание, что хотя запрос SQL подразумевает, что запрашивалось всё содержимое таблицы, метод fetchone вернул только одну строку.

Если повторно вызвать метод, он вернет следующую строку:
```python
In [21]: print(cursor.fetchone())
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
```

Аналогичным образом метод будет возвращать следующие строки.
После обработки всех строк, метод начинает возвращать None.

Засчет этого, метод можно использовать в цикле, например, так:
```python
In [22]: cursor.execute('select * from switch')
Out[22]: <sqlite3.Cursor at 0x104eda810>

In [23]: while True:
   ...:     next_row = cursor.fetchone()
   ...:     if next_row:
   ...:         print(next_row)
   ...:     else:
   ...:         break
   ...:
('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')
('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')
('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str')
('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str')
('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str')
('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')

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
In [24]: print(cursor.arraysize)
1
```

Например, таким образом можно возвращать по три строки из запроса:
```python

In [25]: cursor.execute('select * from switch')
Out[25]: <sqlite3.Cursor at 0x104eda810>

In [26]: from pprint import pprint

In [27]: while True:
    ...:     three_rows = cursor.fetchmany(3)
    ...:     if three_rows:
    ...:         pprint(three_rows)
    ...:     else:
    ...:         break
    ...:
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')]
[('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str')]
[('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]

```

Метод выдает нужное количество строк, а если строк осталось меньше чем параметр size, то оставшиеся строки.

#### Метод fetchall

Метод fetchall возвращает все строки в виде списка:
```python
In [28]: cursor.execute('select * from switch')
Out[28]: <sqlite3.Cursor at 0x104eda810>

In [29]: cursor.fetchall()
Out[29]:
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]

```

Важный аспект работы метода - он возвращает все оставшиеся строки.

То есть, если до метода fetchall, использовался, например, метод fetchone, то метод fetchall вернет оставшиеся строки запроса:
```python
In [30]: cursor.execute('select * from switch')
Out[30]: <sqlite3.Cursor at 0x104eda810>

In [31]: cursor.fetchone()
Out[31]: ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')

In [32]: cursor.fetchone()
Out[32]: ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')

In [33]: cursor.fetchall()
Out[33]:
[('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
 ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]

```

Метод fetchmany, в этом аспекте, работает аналогично.

#### Cursor как итератор

Если нужно построчно обрабатывать результирующие строки, лучше использовать курсор как итератор.
При этом не нужно использовать методы fetch.

При использовании методов execute, возвращается курсор.
А, так как курсор можно использовать как итератор, можно использовать его, например, в цикле for:
```python
In [34]: result = cursor.execute('select * from switch')

In [35]: for row in result:
    ...:     print(row)
    ...:
('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')
('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')
('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str')
('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str')
('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str')
('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')

```


И, конечно же, аналогичный вариант отработает и без присваивания переменной:
```python
In [36]: for row in cursor.execute('select * from switch'):
    ...:     print(row)
    ...:
('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')
('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')
('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str')
('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str')
('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str')
('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')

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

con.execute("""create table switch
            (mac text primary key, hostname text, model text, location text)""")

query = "INSERT into switch values (?, ?, ?, ?)"
con.executemany(query, data)
con.commit()

for row in con.execute("select * from switch"):
    print(row)

con.close()

```

Результат выполнения будет таким:
```
$ python create_sw_inventory_ver1.py
('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')
('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')
```

#### Обработка исключений

Посмотрим на пример использования метода execute, при возникновении ошибки.


В таблице switch поле mac должно быть уникальным.
И, если попытаться записать пересекающийся MAC-адрес, возникнет ошибка:
```python
In [37]: con = sqlite3.connect('sw_inventory2.db')

In [38]: query = "INSERT into switch values ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str')"

In [39]: con.execute(query)
------------------------------------------------------------
IntegrityError             Traceback (most recent call last)
<ipython-input-56-ad34d83a8a84> in <module>()
----> 1 con.execute(query)

IntegrityError: UNIQUE constraint failed: switch.mac
```

Соответственно, можно перехватить исключение:
```python
In [40]: try:
    ...:     con.execute(query)
    ...: except sqlite3.IntegrityError as e:
    ...:     print("Error occured: ", e)
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
# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]


con = sqlite3.connect('sw_inventory3.db')
con.execute("""create table switch
               (mac text primary key, hostname text, model text, location text)""")

try:
    with con:
        query = "INSERT into switch values (?, ?, ?, ?)"
        con.executemany(query, data)

except sqlite3.IntegrityError as e:
    print("Error occured: ", e)

for row in con.execute("select * from switch"):
    print(row)

con.close()
```

Обратите внимание, что хотя транзакция будет откатываться, при возникновении исключения, само исключение всё равно надо перехватывать. 

Для проверки этого функционала, надо записать в таблицу данные, в которых MAC-адрес повторяется.
Но прежде, чтобы не повторять части кода, лучше разнести код в файле create_sw_inventory_ver2.py по функциям (файл create_sw_inventory_ver2_functions.py):
```python
# -*- coding: utf-8 -*-
from pprint import pprint
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]


def create_connection(db_name):
    '''
    Функция создает соединение с БД db_name
    и возвращает его
    '''
    connection = sqlite3.connect(db_name)
    return connection


def write_data_to_db(connection, query, data):
    '''
    Функция ожидает аргументы:
     * connection - соединение с БД
     * query - запрос, который нужно выполнить
     * data - данные, которые надо передать в виде списка кортежей

    Функция пытается записать все данные из списка data.
    Если данные удалось записать успешно, изменения сохраняются в БД
    и функция возвращает True.
    Если в процессе записи возникла ошибка, транзакция откатывается
    и функция возвращает False.
    '''
    try:
        with connection:
            connection.executemany(query, data)
    except sqlite3.IntegrityError as e:
        print("Error occured: ", e)
        return False
    else:
        print("Запись данных прошла успешно")
        return True

def get_all_from_db(connection, query):
    '''
    Функция ожидает аргументы:
     * connection - соединение с БД
     * query - запрос, который нужно выполнить

    Функция возвращает данные полученные из БД.
    '''
    result = [row for row in connection.execute(query)]
    return result


if __name__ == '__main__':
    con = create_connection('sw_inventory3.db')

    print("Создание таблицы...")
    schema = """create table switch
                (mac text primary key, hostname text, model text, location text)"""
    con.execite(schema)

    query_insert = "INSERT into switch values (?, ?, ?, ?)"
    query_get_all = "SELECT * from switch"

    print("Запись данных в БД:")
    pprint(data)
    write_data_to_db(con, query_insert, data)
    print("\nПроверка содержимого БД")
    pprint(get_all_from_db(con, query_get_all))

    con.close()

```

Результат выполнения скрипта выглядит так:
```
$ python create_sw_inventory_ver2_functions.py
Создание таблицы...
Запись данных в БД:
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]
Запись данных прошла успешно

Проверка содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

```


Теперь проверим как функция write_data_to_db отработает при наличии одинаковых MAC-адресов в данных.

В файле create_sw_inventory_ver3.py используются функции из файла create_sw_inventory_ver2_functions.py и подразумемается, что скрипт будет запускаться, после записи предыдущих данных:
```python
# -*- coding: utf-8 -*-
from pprint import pprint
import sqlite3
import create_sw_inventory_ver2_functions as dbf

#MAC-адрес sw7 совпадает с MAC-адресом коммутатора sw3 в списке data
data2 = [('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
         ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
         ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
         ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]

con = dbf.create_connection('sw_inventory3.db')

query_insert = "INSERT into switch values (?, ?, ?, ?)"
query_get_all = "SELECT * from switch"

print("\nПроверка текущего содержимого БД")
pprint(dbf.get_all_from_db(con, query_get_all))

print('-'*60)
print("Попытка записать данные с повторяющимся MAC-адресом:")
pprint(data2)
dbf.write_data_to_db(con, query_insert, data2)
print("\nПроверка содержимого БД")
pprint(dbf.get_all_from_db(con, query_get_all))

con.close()

```

В списке data2 у коммутатора sw7 MAC-адрес совпадает с уже существующим в БД коммутатором sw3.

Результат выполнения скрипта:
```
$ python create_sw_inventory_ver3.py

Проверка текущего содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]
------------------------------------------------------------
Попытка записать данные с повторяющимся MAC-адресом:
[('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
 ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
 ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]
Error occured:  UNIQUE constraint failed: switch.mac

Проверка содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

```

Обратите внимание, что содержимое таблицы switch до и после добавления информации - одинаково.
Это значит, что не записалась ни одна строка из списка data2.

Так получилось из-за того, что используется метод executemany и
в пределах одной транзакции мы пытаемся записать все 4 строки.
Если возникает ошибка с одной из них - откатываются все изменения.

Иногда, это именно то поведение, которое нужно.
Если же надо чтобы игнорировались только строки с ошибками, надо использовать метод execute и записывать каждую строку отдельно.

В файле create_sw_inventory_ver4.py создана функция write_rows_to_db, которая уже поочереди пишет данные и, если возникла ошибка, то только изменения для конкретных данных откатываются:
```python
# -*- coding: utf-8 -*-
from pprint import pprint
import sqlite3
import create_sw_inventory_ver2_functions as dbf

#MAC-адрес sw7 совпадает с MAC-адресом коммутатора sw3 в списке data
data2 = [('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
         ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
         ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
         ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]


def write_rows_to_db(connection, query, data, verbose=False):
    '''
    Функция ожидает аргументы:
     * connection - соединение с БД
     * query - запрос, который нужно выполнить
     * data - данные, которые надо передать в виде списка кортежей

    Функция пытается записать поочереди кортежи из списка data.
    Если кортеж удалось записать успешно, изменения сохраняются в БД.
    Если в процессе записи кортежа возникла ошибка, транзакция откатывается.

    Флаг verbose контролирует то, будут ли выведены сообщения об удачной
    или неудачной записи кортежа.
    '''
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as e:
            if verbose:
                print('При записи данных "{}" возникла ошибка'.format(', '.join(row), e))
        else:
            if verbose:
                print('Запись данных "{}" прошла успешно'.format(', '.join(row)))


con = dbf.create_connection('sw_inventory3.db')

query_insert = 'INSERT into switch values (?, ?, ?, ?)'
query_get_all = 'SELECT * from switch'

print('\nПроверка текущего содержимого БД')
pprint(dbf.get_all_from_db(con, query_get_all))

print('-'*60)
print('Попытка записать данные с повторяющимся MAC-адресом:')
pprint(data2)
write_rows_to_db(con, query_insert, data2, verbose=True)
print('\nПроверка содержимого БД')
pprint(dbf.get_all_from_db(con, query_get_all))

con.close()

```

Теперь результат выполнения будет таким (пропущен только sw7):
```
$ python create_sw_inventory_ver4.py

Проверка текущего содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]
------------------------------------------------------------
Попытка записать данные с повторяющимся MAC-адресом:
[('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
 ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
 ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]
Запись данных "0055.AAAA.CCCC, sw5, Cisco 3750, London, Green Str" прошла успешно
Запись данных "0066.BBBB.CCCC, sw6, Cisco 3780, London, Green Str" прошла успешно
При записи данных "0000.AAAA.DDDD, sw7, Cisco 2960, London, Green Str" возникла ошибка
Запись данных "0088.AAAA.CCCC, sw8, Cisco 3750, London, Green Str" прошла успешно

Проверка содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str'),
 ('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
 ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
 ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]

```

