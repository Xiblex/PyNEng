### WHERE

Оператор WHERE используется для уточнения запроса.
С помощью этого оператора можно указывать определенные условия, по которым отбираются данные.
Если условие выполнено, возвращается соответствующее значение из таблицы, если нет, не возвращается.

Например, таблица switch выглядит так:
```sql
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
0000.2222.CCCC  sw2         Cisco 3750  London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.4444.CCCC  sw4         Cisco 3650  London, Green Str  10.255.0.4  255         MNGMT      
```

Показать только те коммутаторы, модель которых 3750:
```sql
sqlite> SELECT * from switch WHERE model = 'Cisco 3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.2222.CCCC  sw2         Cisco 3750  London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

Оператор where позволяет указывать не только конкретное значение поля.
Если добавить к нему оператор like, можно указывать шаблон поля.

LIKE с помощью символов ```_``` и ```%``` указывает на что должно быть похоже значение:
* ```_``` - обозначает один символ или число
* ```%``` - обозначает ноль, один или много символов

Например, если поле model записано в разном формате, с помощью предыдущего запроса, не получится вывести нужные коммутаторы.

Например, если в таблице поле model записано в разном формате:
```sql
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.4444.CCCC  sw4         Cisco 3650  London, Green Str  10.255.0.4  255         MNGMT      
```

В таком варианте предыдущий запрос с оператором WHERE не поможет:
```sql
sqlite> SELECT * from switch WHERE model = 'Cisco 3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

Но, если вместе с оператором WHERE использовать оператор ```LIKE```:
```sql
sqlite> SELECT * from switch WHERE model LIKE '%3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

