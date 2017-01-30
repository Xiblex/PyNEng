### ALTER

Оператор alter позволяет менять существующую таблицу: добавлять новые колонки или переименовывать таблицу.


Добавим в таблицу новые поля:
* mngmt_ip - IP-адрес коммутатора в менеджмент VLAN
* mngmt_vid - VLAN ID (номер VLAN) для менеджмент VLAN
* mngmt_vname - Имя VLAN, который используется для менеджмента

Добавление записей с помощью команды ALTER:
```sql
sqlite> ALTER table switch ADD COLUMN mngmt_ip text;
sqlite> ALTER table switch ADD COLUMN mngmt_vid varchar(10);
sqlite> ALTER table switch ADD COLUMN mngmt_vname  text;
```

Теперь таблица выглядит так (новые поля установлены в значение NULL):
```sql
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str                                     
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str                                    
```

