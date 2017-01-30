### ORDER BY

И еще один полезный оператор ORDER BY.
Он используется для сортировки вывода по определенному полю, по возрастанию или убыванию.

Например, выведем все записи в таблице switch и отсортируем их по имени коммутаторов (по умолчанию выполняется сортировка по умолчанию, поэтому параметр ASC можно не указывать):
```sql
sqlite> SELECT * from switch ORDER BY hostname ASC;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
```

