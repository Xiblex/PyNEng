##Работа с файлами в формате JSON

JSON (JavaScript Object Notation) - это текстовый формат для хранения и обмена данными.

[JSON](https://ru.wikipedia.org/wiki/JSON) по синтаксису очень похож на словари в Python. И достаточно удобен для восприятия.

Как и в случае с CSV, в Python есть модуль, который позволяет легко записывать и читать данные в формате JSON.

###Чтение
Начнем с чтения файла в формате JSON.

Файл sw_templates.json:
```json
{
  "access": [
    "switchport mode access", 
    "switchport access vlan", 
    "switchport nonegotiate", 
    "spanning-tree portfast", 
    "spanning-tree bpduguard enable"
  ], 
  "trunk": [
    "switchport trunk encapsulation dot1q", 
    "switchport mode trunk", 
    "switchport trunk native vlan 999", 
    "switchport trunk allowed vlan"
  ]
}
```

Попробуем считать содержимое файла в объект Python:
```python
In [1]: import json

In [2]: templates = json.load(open('sw_templates.json'))

In [3]: print templates
{u'access': [u'switchport mode access', u'switchport access vlan', u'switchport nonegotiate', u'spanning-tree portfast', u'spanning-tree bpduguard enable'], u'trunk': [u'switchport trunk encapsulation dot1q', u'switchport mode trunk', u'switchport trunk native vlan 999', u'switchport trunk allowed vlan']}

In [4]: for section, commands in templates.items():
   ...:     print section
   ...:     print '\n'.join(commands)
   ...:
access
switchport mode access
switchport access vlan
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
trunk
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 999
switchport trunk allowed vlan
```

В итоге мы получили словарь. Обратите внимание, что при чтении из файла в формате JSON мы получили unicode.


###Запись

Запись файла в формате JSON также осуществляется достаточно легко.

Попробуем записать аналогичный словарь в файл:
```python
import json


trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']


access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_json = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.json', 'w') as f:
    f.write(json.dumps(to_json))

with open('sw_templates.json') as f:
    print f.read()
```

Последние две строки выводят содержимое файла sw_templates.json. Теперь файл выглядит таким образом:
```json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate", "spanning-tree portfast", "spanning-tree bpduguard enable"], "trunk": ["switchport trunk encapsulation dot1q", "switchport mode trunk", "switchport trunk native vlan 999", "switchport trunk allowed vlan"]}
```

Формат получился не такой, как мы видели выше.

Такой формат менее удобно воспринимать, но к счастью, модуль json позволяет управлять подобными вещами.

Передав дополнительные параметры методу dumps, мы получаем более удобный для чтение вывод:
```python
import json


trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']


access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_json = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.json', 'w') as f:
    f.write(json.dumps(to_json, sort_keys=True, indent=2))

with open('sw_templates.json') as f:
    print f.read()
``` 

Теперь содержимое файла sw_templates.json выглядит так:
```json
{
  "access": [
    "switchport mode access",
    "switchport access vlan",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable"
  ],
  "trunk": [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan"
  ]
}
```

Еще один важный аспект преобразования данных в формат json: данные не всегда будут того же типа, что исходные данные в Python.

Мы уже видели это со строками - мы получили при чтении unicode.

Кроме того, при записи в JSON кортежей, они превращаются в списки.

Например:
```python

In [1]: import json

In [2]: trunk_template = ('switchport trunk encapsulation dot1q',
   ...:                   'switchport mode trunk',
   ...:                   'switchport trunk native vlan 999',
   ...:                   'switchport trunk allowed vlan')

In [3]: print type(trunk_template)
<type 'tuple'>

In [4]: with open('trunk_template.json', 'w') as f:
   ...:     f.write(json.dumps(trunk_template, sort_keys=True, indent=2))
   ...:

In [5]: cat trunk_template.json
[
  "switchport trunk encapsulation dot1q",
  "switchport mode trunk",
  "switchport trunk native vlan 999",
  "switchport trunk allowed vlan"
]
In [6]: templates = json.load(open('trunk_template.json'))

In [7]: type(templates)
Out[7]: list

In [8]: print templates
[u'switchport trunk encapsulation dot1q', u'switchport mode trunk', u'switchport trunk native vlan 999', u'switchport trunk allowed vlan']
```

