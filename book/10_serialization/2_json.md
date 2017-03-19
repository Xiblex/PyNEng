##Работа с файлами в формате JSON

__JSON (JavaScript Object Notation)__ - это текстовый формат для хранения и обмена данными.

[JSON](https://ru.wikipedia.org/wiki/JSON) по синтаксису очень похож на словари в Python. И достаточно удобен для восприятия.

Как и в случае с CSV, в Python есть модуль, который позволяет легко записывать и читать данные в формате JSON.

###Чтение

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

Для чтения, в модуле json есть два метода:
* json.load() - метод считывает файл и возвращает объекты Python
* json.loads() - метод считывает строку в формате JSON и возвращает объекты Python

#### json.load()

Чтение файла в объект Python:
```python
In [1]: import json

In [2]: with open('sw_templates.json') as f:
   ...:     templates = json.load(f)
   ...:

In [3]: templates
Out[3]:
{u'access': [u'switchport mode access',
  u'switchport access vlan',
  u'switchport nonegotiate',
  u'spanning-tree portfast',
  u'spanning-tree bpduguard enable'],
 u'trunk': [u'switchport trunk encapsulation dot1q',
  u'switchport mode trunk',
  u'switchport trunk native vlan 999',
  u'switchport trunk allowed vlan']}

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

Результат чтения - словарь.
Обратите внимание, что при чтении из файла в формате JSON, строки будут в unicode.

> Мы не будем рассматривать работу с Unicode. Хороший документ о работе с unicode: [Unicode HowTo](https://docs.python.org/2/howto/unicode.html).

#### json.loads()

Считывание строки в формате JSON в объект Python:
```python
In [5]: with open('sw_templates.json') as f:
   ...:     templates = json.loads(f.read())
   ...:

In [6]: templates
Out[6]:
{u'access': [u'switchport mode access',
  u'switchport access vlan',
  u'switchport nonegotiate',
  u'spanning-tree portfast',
  u'spanning-tree bpduguard enable'],
 u'trunk': [u'switchport trunk encapsulation dot1q',
  u'switchport mode trunk',
  u'switchport trunk native vlan 999',
  u'switchport trunk allowed vlan']}
```

###Запись

Запись файла в формате JSON также осуществляется достаточно легко.

Для записи информации в формате JSON в модуле json также два метода:
* json.dump() - метод записывает объект Python в файл, в формате JSON
* json.dumps() - метод возвращает строку в формате JSON

#### json.dump()

Запись объекта Python в файл:
```python
In [7]: trunk_template = ['switchport trunk encapsulation dot1q',
   ...:                   'switchport mode trunk',
   ...:                   'switchport trunk native vlan 999',
   ...:                   'switchport trunk allowed vlan']
   ...:
   ...:
   ...: access_template = ['switchport mode access',
   ...:                    'switchport access vlan',
   ...:                    'switchport nonegotiate',
   ...:                    'spanning-tree portfast',
   ...:                    'spanning-tree bpduguard enable']
   ...:
   ...: to_json = {'trunk':trunk_template, 'access':access_template}
   ...:

In [8]: with open('sw_templates.json', 'w') as f:
   ...:     json.dump(to_json, f)
   ...:

In [9]: cat sw_templates.json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate", "spanning-tree portfast", "spanning-tree bpduguard enable"], "trunk": ["switchport trunk encapsulation dot1q", "switchport mode trunk", "switchport trunk native vlan 999", "switchport trunk allowed vlan"]}
```

Когда нужно записать информацию в формате JSON в файл, лучше использовать метод dump.

#### json.dumps()

Преобразование объекта в строку в формате JSON:
```python
In [10]: with open('sw_templates.json', 'w') as f:
    ...:     f.write(json.dumps( to_json ))
    ...:

In [11]: cat sw_templates.json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate", "spanning-tree portfast", "spanning-tree bpduguard enable"], "trunk": ["switchport trunk encapsulation dot1q", "switchport mode trunk", "switchport trunk native vlan 999", "switchport trunk allowed vlan"]}
```

Метод json.dumps() подходит для ситуаций, когда надо вернуть строку в формате JSON. 


#### Дополнительные параметры методов записи

Методам dump и dumps можно передавать дополнительные параметры для управления форматом вывода.

По умолчанию эти методы записывают информацию в компактном представлении.
Как правило, когда данные используются другими программами, визуальное представление данных не важно.
Если же данные в файле нужно будет считать человеку, такой формат не очень удобно воспринимать.

К счастью, модуль json позволяет управлять подобными вещами.

Передав дополнительные параметры методу dump (или методу dumps), можно получить более удобный для чтение вывод (файл json_write_ver2.py):
```python
In [13]: with open('sw_templates.json', 'w') as f:
    ...:     json.dump(to_json, f, sort_keys=True, indent=2)
    ...:
```

Теперь содержимое файла sw_templates.json выглядит так:
```
In [14]: cat sw_templates.json
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


#### Изменение типа данных
Еще один важный аспект преобразования данных в формат json: данные не всегда будут того же типа, что исходные данные в Python.

Такая ситуация уже возникала со строками - они были в формате unicode.
Кроме того, при записи в JSON кортежей, они превращаются в списки.

Например:
```python

In [15]: import json

In [16]: trunk_template = ('switchport trunk encapsulation dot1q',
    ...:                   'switchport mode trunk',
    ...:                   'switchport trunk native vlan 999',
    ...:                   'switchport trunk allowed vlan')

In [17]: print type(trunk_template)
<type 'tuple'>

In [18]: with open('trunk_template.json', 'w') as f:
    ...:     json.dump(trunk_template, f, sort_keys=True, indent=2)
    ...:

In [19]: cat trunk_template.json
[
  "switchport trunk encapsulation dot1q",
  "switchport mode trunk",
  "switchport trunk native vlan 999",
  "switchport trunk allowed vlan"
]
In [20]: templates = json.load(open('trunk_template.json'))

In [21]: type(templates)
Out[21]: list

In [22]: print templates
[u'switchport trunk encapsulation dot1q', u'switchport mode trunk', u'switchport trunk native vlan 999', u'switchport trunk allowed vlan']
```

#### Ограничение по типам данных

В формат JSON нельзя записать словарь у которого ключи - кортежи:
```python
In [23]: to_json = { ('trunk', 'cisco'): trunk_template, 'access': access_template}

In [24]: with open('sw_templates.json', 'w') as f:
    ...:     json.dump(to_json, f)
    ...:
...
TypeError: key ('trunk', 'cisco') is not a string
```

Но, с помощью дополнительного параметра можно игнорировать подобные ключи:
```python
In [25]: to_json = { ('trunk', 'cisco'): trunk_template, 'access': access_template}

In [26]: with open('sw_templates.json', 'w') as f:
    ...:     json.dump(to_json, f, skipkeys=True)
    ...:
    ...:

In [27]: cat sw_templates.json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate", "spanning-tree portfast", "spanning-tree bpduguard enable"]}
```


