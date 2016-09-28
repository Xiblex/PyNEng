##Работа с файлами в формате CSV

CSV (comma-separated value) - это формат представления табличных данных (например, это могут быть данные из таблицы, или данные из БД).

В этом формате, каждая строка файла - это строка таблицы.

Несмотря на название формата, разделителем может быть не только запятая.

И, хотя у форматов с другим разделителем может быть и собственное название, например, TSV (tab separated values), тем не менее под форматом CSV понимают, как правило, любые разделители.


Пример файла в формате CSV:
```
hostname,vendor,model,location
sw1,Cisco,3750,London
sw2,Cisco,3850,Liverpool
sw3,Cisco,3650,Liverpool
sw4,Cisco,3650,London
```

В стандартной библиотеке Python есть модуль csv, который позволяет работать с файлами в CSV формате.

###Чтение


Пример использования модуля csv:
```python
import csv

with open('sw_data.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print row
```

Вывод будет таким:
```
['hostname', 'vendor', 'model', 'location']
['sw1', 'Cisco', '3750', 'London']
['sw2', 'Cisco', '3850', 'Liverpool']
['sw3', 'Cisco', '3650', 'Liverpool']
['sw4', 'Cisco', '3650', 'London']
```

В первом списке мы получаем названия столбцов, а в остальных, соответствующие значения.

Иногда в результате обработки, гораздо удобней получить словари, в которых ключи - это названия столбцов, а значения - значения столбцов.

Для этого в модуле есть __DictReader__:
```python
import csv

with open('sw_data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print row
```

Вывод будет таким:
```
{'model': '3750', 'hostname': 'sw1', 'vendor': 'Cisco', 'location': 'London'}
{'model': '3850', 'hostname': 'sw2', 'vendor': 'Cisco', 'location': 'Liverpool'}
{'model': '3650', 'hostname': 'sw3', 'vendor': 'Cisco', 'location': 'Liverpool'}
{'model': '3650', 'hostname': 'sw4', 'vendor': 'Cisco', 'location': 'London'}
```

Обратите внимание, что сам reader это итератор. Поэтому, если просто вывести reader, то мы получим такой вывод:
```python
In [1]: import csv

In [2]: with open('sw_data.csv') as f:
   ...:     reader = csv.reader(f)
   ...:     print reader
   ...:
<_csv.reader object at 0x10385b050>
```

Но можно таким образом превратить его в список, если нужно все объекты передать куда-то дальше:
```python
In [3]: with open('sw_data.csv') as f:
   ...:     reader = csv.reader(f)
   ...:     print list(reader)
   ...:
[['hostname', 'vendor', 'model', 'location'], ['sw1', 'Cisco', '3750', 'London'], ['sw2', 'Cisco', '3850', 'Liverpool'], ['sw3', 'Cisco', '3650', 'Liverpool'], ['sw4', 'Cisco', '3650', 'London']]
```

###Запись

Аналогичным образом, с помощью модуля csv, можно и записать файл в формате CSV.

```python
import csv

data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]

with open('sw_data_new.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

with open('sw_data_new.csv') as f:
    print f.read()
```

В это примере мы сперва записываем строки списка в файл, а затем отображаем содержимое файла.

Вывод будет таким:
```
hostname,vendor,model,location
sw1,Cisco,3750,"London, Best str"
sw2,Cisco,3850,"Liverpool, Better str"
sw3,Cisco,3650,"Liverpool, Better str"
sw4,Cisco,3650,"London, Best str"
```

Обратите внимание на интересную особенность: последнее значение, взято в кавычки, а остальные строки - нет.

Но было бы лучше, чтобы все строки были в кавычках. Конечно, в этом случае, у нас достаточно простой пример, но когда в строках больше значений, то кавычки позволяют указать где начинается и заканчивается значение.

Обратите внимание, что внутри кавычек, в последних строках у нас тоже присутствует запятая. Несмотря на это, если бы мы считывали этот файл, он бы корректно прочитался. Так как запятые внутри кавычек не воспринимаются как разделитель.

Но, было бы лучше, чтобы все строки были в кавычках. Модуль позволяет управлять этим. Для того, чтобы все строки записывались в файл csv с кавычками, надо изменить наш скрипт так:
```python
import csv

data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]

with open('sw_data_new.csv', 'w') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in data:
        writer.writerow(row)

with open('sw_data_new.csv') as f:
    print f.read()
```

Теперь вывод будет таким:
```
"hostname","vendor","model","location"
"sw1","Cisco","3750","London, Best str"
"sw2","Cisco","3850","Liverpool, Better str"
"sw3","Cisco","3650","Liverpool, Better str"
"sw4","Cisco","3650","London, Best str"
```

Теперь все значения с кавычками (так как номер модели задан как строка, в изначальном списке, тут он тоже в кавычках).

###Указание разделителя

Иногда, в качестве разделителя используются другие значения. В таком случае, должна быть возможность подсказать модулю, какой именно разделитель использовать.

Например, если в файле используется разделитель ';':
```
hostname;vendor;model;location
sw1;Cisco;3750;London
sw2;Cisco;3850;Liverpool
sw3;Cisco;3650;Liverpool
sw4;Cisco;3650;London
```

Достаточно просто указать какой разделитель используется в reader:
```python
import csv

with open('sw_data2.csv') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        print row
```
