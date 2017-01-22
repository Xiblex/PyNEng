### ALTER
Теперь попробуем изменить таблицу. Добавим новые поля в таблицу switch.

Добавим в определение таблицы такие новые поля:
* mngmt_ip - IP-адрес коммутатора в менеджмент VLAN
* mngmt_vid - VLAN ID (номер VLAN) для менеджмент VLAN
* mngmt_vname - Имя VLAN, который используется для менеджмента

Добавление записей выполняется с помощью DDL, используя команду ALTER:
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

Если в процессе выполнения задания надо будет удалить неправильную запись, можно использовать команду (изменив по аналогии):
```sql
delete from switch where mngmt_vid = 255;
```

В итоге таблица должна выглядеть так:
```sql
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
```
