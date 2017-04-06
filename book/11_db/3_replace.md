### REPLACE

Оператор replace используется для добавления или замены данных в таблице.

> Оператор replace может поддерживаться не во всех СУБД.

Когда возникает нарушение условия уникальности поля, выражение с оператором replace:
* удаляет существующую строку, которая вызвала нарушение
* добавляет новую строку

У выражения replace есть два вида:
```
sqlite> INSERT OR REPLACE INTO switch
   ...> VALUES ('0000.DDDD.CCCC', 'sw4', 'Cisco 3850', 'London, Green Str');
```

Или более короткий вариант:
```
sqlite> REPLACE INTO switch
   ...> VALUES ('0000.DDDD.CCCC', 'sw4', 'Cisco 3850', 'London, Green Str');
```

#### Пример использования оператора replace

Пример таблицы:
```
sqlite> create table switch (mac text primary key, hostname text, model text, location text);
sqlite> INSERT into switch values ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str');
sqlite> INSERT into switch values ('0000.BBBB.CCCC', 'sw2', 'Cisco 3850', 'London, Green Str');
sqlite> INSERT into switch values ('0000.CCCC.CCCC', 'sw3', 'Cisco 3850', 'London, Green Str');

sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3850  London, Green Str
0000.CCCC.CCCC  sw3         Cisco 3850  London, Green Str
```

При добавлении записи, для которой не возникает нарушения уникальности поля, replace работает как обычный insert:
```
sqlite> replace into switch values ('0000.DDDD.CCCC', 'sw4', 'Cisco 3850', 'London, Green Str');

sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3850  London, Green Str
0000.CCCC.CCCC  sw3         Cisco 3850  London, Green Str
0000.DDDD.CCCC  sw4         Cisco 3850  London, Green Str
```

Но, если возникает нарушение, выполняется замена:
```
sqlite> insert or replace into switch values ('0000.DDDD.CCCC', 'sw5', 'Cisco 3850', 'London, Green Str');

sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3850  London, Green Str
0000.CCCC.CCCC  sw3         Cisco 3850  London, Green Str
0000.DDDD.CCCC  sw5         Cisco 3850  London, Green Str
```

В данном случае MAC-адрес в новой записи совпадает с уже существующей, поэтому происходит замена.


Если были указаны не все поля, в новой записи будут только те поля, которые были указаны:
```
sqlite> replace into switch (mac, hostname, model)
   ...> values ('0000.DDDD.CCCC', 'sw5', 'Cisco 3850');

sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3850  London, Green Str
0000.CCCC.CCCC  sw3         Cisco 3850  London, Green Str
0000.DDDD.CCCC  sw5         Cisco 3850
```

Это связано с тем, что replace сначала удаляет существующую запись.


