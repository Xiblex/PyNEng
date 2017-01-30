### UPDATE

Оператор update используется для изменения существующей записи таблицы.

Обычно, update используется вместе с оператором where, чтобы уточнить какую именно запись необходимо изменить.

Например, предположим, что sw1 был заменен с модели 3750 на модель 3850.
Соответственно, изменилось не только поле модель, но и поле MAC-адрес.

Внесение изменений:
```sql
sqlite> UPDATE switch set model = 'Cisco 3850' where hostname = 'sw1';
sqlite> UPDATE switch set mac = '0000.DDDD.DDDD' where hostname = 'sw1';
```

Результат будет таким:
```
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
```

