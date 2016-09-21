## Пример использования Jinja с корректным использованием программного интерфейса


> Для того чтобы разобраться с Jinja2, лучше использовать предыдущие примеры.

> Этот вариант показан для того, чтобы показать, в каком виде предыдущий пример, скорее всего, встретится в реальной жизни. И как, в таком случае, обрабатывать вводные данные и шаблон.



Термин "программный интерфейс" относится к способу работы Jinja с вводными данными и шаблоном, для генерации итоговых файлов. 


Ранее для загрузки шаблона, мы использовали класс Template и, уже в самом файле, указывали, что это шаблон. А затем его импортировали.

Такой вариант проще всего понять, однако, в реальной жизни, лучше использовать другой способ:
* будет лучше, если шаблон будет простым текстовым файлом
* для того чтобы загрузить шаблон, используем:
 * Loader (загрузчик):
   * позволяет указать путь (или пути) к шаблонам
 * Environment (окружение) позволяет:
   * указывать где искать шаблоны, с помощью загрузчика
   * указывать дополнительные параметры обработки шаблона
   * использовать методы Environment, для того чтобы указать как именно обрабатывать шаблон

Подробнее о программном интерфейсе Jinja2 можно почитать на странице [Jinja2](xgu.ru/wiki/Jinja2).


Кроме изменения шаблона и собственно скрипта, переделаем также формат вводных данных:
* данные записаны в файле просто в виде строк, через запятую
 * для того чтобы не надо было описывать их в синтаксисе объектов Python  и не надо было писать кавычки и так далее
* при обработке данных из файла, мы превратим их в списки, а затем обработаем списки
* для этого воспользуемся примером генерации словарей из списков, который рассматривался в разделе "Словари"
* обратите внимание, что тут используется несколько приемов, которые мы изучали ранее и, чтобы понять скрипт, может потребоваться пересмотреть предыдущие темы

Переделанный пример предыдущего скрипта, шаблона и файла с данными:

Шаблон router_template.txt
```
hostname {{name}}
!
interface Loopback10
 description MPLS loopback
 ip address 10.10.{{id}}.1 255.255.255.255
 !
interface GigabitEthernet0/0
 description WAN to {{name}} sw1 G0/1
!
interface GigabitEthernet0/0.1{{id}}1
 description MPLS to {{to_name}}
 encapsulation dot1Q 1{{id}}1
 ip address 10.{{id}}.1.2 255.255.255.252
 ip ospf network point-to-point
 ip ospf hello-interval 1
 ip ospf cost 10
!
interface GigabitEthernet0/1
 description LAN {{name}} to sw1 G0/2 !
interface GigabitEthernet0/1.{{IT}}
 description PW IT {{name}} - {{to_name}}
 encapsulation dot1Q {{IT}}
 xconnect 10.10.{{to_id}}.1 {{id}}11 encapsulation mpls
 backup peer 10.10.{{to_id}}.2 {{id}}21
  backup delay 1 1
!
interface GigabitEthernet0/1.{{BS}}
 description PW BS {{name}} - {{to_name}}
 encapsulation dot1Q {{BS}}
 xconnect 10.10.{{to_id}}.1 {{to_id}}{{id}}11 encapsulation mpls
  backup peer 10.10.{{to_id}}.2 {{to_id}}{{id}}21
  backup delay 1 1
!
router ospf 10
 router-id 10.10.{{id}}.1
 auto-cost reference-bandwidth 10000
 network 10.0.0.0 0.255.255.255 area 0
 !
```

Файл с данными routers_info.txt
```
id,name,to_name,IT,BS,to_id
11,Liverpool,LONDON,791,1550,1
12,Bristol,LONDON,793,1510,1
14,Coventry,Manchester,892,1650,2
```


Скрипт для генерации конфигураций router_config_generator.py
```python
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('router_template.txt')

with open('routers_info.txt','r') as file:
    data = [line.strip().split(',') for line in file]

routers = [dict(zip(data[0],i)) for i in data[1:]]

for router in routers:
    r1_conf = router['name']+'_r1'
    with open(r1_conf,'w') as f:
        f.write(template.render( router ))
```


Файл router_config_generator.py импортирует из модуля jinja2:
* __FileSystemLoader__ - загрузчик, который позволяет работать с файловой системой
 * тут указывается путь к каталогу, где находятся шаблоны
 * в данном случае, шаблон находится в каталоге templates
* __Environment__ - класс для описания параметров окружения:
 * в данном случае, указан только загрузчик

Обратите внимание, что шаблон теперь находится в каталоге __templates__.

Для того чтобы указать текущий каталог в  загрузчике, надо добавить пару строк и изменить значение в загручике:
```python
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader = FileSystemLoader(curr_dir))
```


Метод __get_template()__ используется для того, чтобы получить шаблон. В скобках указывается имя файла.

Затем мы открываем файл с данными (routers_info.txt):
* используем генератор списков для того чтобы создать список списков (где каждый вложенный список это список слов в исходной строке):
 * генератор списков - перебираем строки файла
 * __strip()__ - удаляем символ \n в конце строки
 * __split(',')__ - разделяем строку в список элементов, взяв как разделитель запятую
* далее снова используем list comprehension для того чтобы создать список словарей
 * словари создаются из комбинации двух списков:
   * первый список в списке data - это ключи, которые используются в словарях
   * остальные списки это наборы данных
 * как использовать __dict__ и __zip__, можно посмотреть в подразделе "Словарь из двух списков (advanced)"

Последняя часть осталась неизменной.

В дальнейшем, в практических примерах, мы будем использовать такой вариант.
