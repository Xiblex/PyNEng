### SELECT
Теперь в нашей таблице две записи. Просмотрим их:
```
sqlite> SELECT * from switch;
0000.AAAA.CCCC|sw1|Cisco 3750|London, Green Str
0000.BBBB.CCCC|sw5|Cisco 3850|London, Green Str
```

В данном случае мы отображаем все записи в таблице switch.

В отображении таблицы не хватает названия полей. Включить их отображение можно с помощью команды __.headers ON__.
```
sqlite> .headers ON
sqlite> SELECT * from switch;
mac|hostname|model|location
0000.AAAA.CCCC|sw1|Cisco 3750|London, Green Str
0000.BBBB.CCCC|sw5|Cisco 3850|London, Green Str
```

Заголовки отобразились, но в целом отображение не очень приятное. Хотелось бы, чтобы все выводилось в виде колонок. За форматирование вывода отвечает команда __.mode__.

Нам нужен режим __.mode column__:
```
sqlite> .mode column
sqlite> SELECT * from switch;
mac             hostname    model       location         
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str
```

При желании, можно выставить и ширину колонок. Для этого используется команда __.width__. Например, попробуйте выставить .width 20.
