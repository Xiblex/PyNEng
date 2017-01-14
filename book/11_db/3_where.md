### WHERE
Оператор WHERE используется для уточнения запроса. С помощью этого оператора мы можем указывать определенные условия, по которым отбираются данные. Если условие выполнено, возвращается соответствующее значение из таблицы, если нет, не возвращается.

Например, наша таблица с коммутаторами немного разрослась:
```
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
0000.2222.CCCC  sw2         Cisco 3750  London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.4444.CCCC  sw4         Cisco 3650  London, Green Str  10.255.0.4  255         MNGMT      
```

Воспользуется оператором WHERE и отфильтруем вывод. Отобразим информацию только о тех коммутаторах, модель которых 3750:
```
sqlite> SELECT * from switch WHERE model = 'Cisco 3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.2222.CCCC  sw2         Cisco 3750  London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

В данном случае нам пришлось писать полностью все строку, которая соответствет полю model. Если бы поле было записано в разном формате, то мы бы уже не смогли таким образом вывести нужные коммутаторы.

Например, если в таблице поле model записано в разном формате:
```
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.4444.CCCC  sw4         Cisco 3650  London, Green Str  10.255.0.4  255         MNGMT      
```

В таком варианте предыдущий запрос с оператором WHERE нам не поможет:
```
sqlite> SELECT * from switch WHERE model = 'Cisco 3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

Но вместе с оператором WHERE мы можем использовать оператор __LIKE__:
```
sqlite> SELECT * from switch WHERE model LIKE '%3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

LIKE с помощью символов '_' и '%' указывает на что должно быть похоже значение:
* '_' - обозначает один символ или число
* '%' - обозначает ноль, один или много символов
