### SELECT

Оператор select позволяет запрашивать информацию в таблице.

Например:
```sql
sqlite> SELECT * from switch;
0000.AAAA.CCCC|sw1|Cisco 3750|London, Green Str
0000.BBBB.CCCC|sw5|Cisco 3850|London, Green Str
```

```select *``` означает, что нужно вывести все поля таблицы.
Следом, указывается из какой таблицы запрашиваются данные: ```from switch```.

В данном случае, в отображении таблицы не хватает названия полей.
Включить это можно с помощью команды ```.headers ON```.
```sql
sqlite> .headers ON
sqlite> SELECT * from switch;
mac|hostname|model|location
0000.AAAA.CCCC|sw1|Cisco 3750|London, Green Str
0000.BBBB.CCCC|sw5|Cisco 3850|London, Green Str
```

Теперь отобразились заголовки, но в целом, отображение не очень приятное.
Хотелось бы, чтобы все выводилось в виде колонок.
За форматирование вывода отвечает команда ```.mode```.

Режим ```.mode column``` включает отображение в виде колонок:
```sql
sqlite> .mode column
sqlite> SELECT * from switch;
mac             hostname    model       location         
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str
```

При желании, можно выставить и ширину колонок.
Для этого используется команда ```.width```.
Например, попробуйте выставить ```.width 20```.
