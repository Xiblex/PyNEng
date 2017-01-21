##Работа с файлами в формате YAML

__YAML (YAML Ain't Markup Language)__ - еще один текстовый формат для записи данных.

YAML более приятен для восприятия человеком, чем JSON.

###Синтаксис YAML

> Мы подробнее останавливаемся на синтаксисе YAML, так как он чаще используется для передачи каких-то параметров вручную. И, кроме того, playbook Ansible используют YAML для описания действий.

Как и Python, YAML использует отступы для указания структуры документа.
Но в YAML можно использовать только пробелы и нельзя использовать знаки табуляции.

Еще одна схожесть с Python: комментарии начинаются с символа # и продолжаются до конца строки.


Пройдемся по тому как в YAML записываются различные форматы данных.

####Список

Список может быть записан в одну строку:
```yaml
[switchport mode access, switchport access vlan, switchport nonegotiate, spanning-tree portfast, spanning-tree bpduguard enable]
```

Или каждый элемент списка в своей строке:
```yaml
- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable
```

Когда список записан таким блоком, каждая строка должна начинаться с ```- ``` (минуса и пробела). И все строки в списке должны быть на одном уровне отступа.

####Словарь

Словарь также может быть записан в одну строку:
```yaml
{ vlan: 100, name: IT }
```

Или блоком:
```yaml
vlan: 100
name: IT
```

####Строки

Наверняка вы обратили внимание, что строки в YAML не обязательно брать в кавычки. Это удобно и приятно, но иногда всё же следует использовать кавычки. Например, когда в строке используется какой-то специальный символ (специальный для YAML).

Например, такую строку нужно взять в кавычки, чтобы она была корректно воспринята YAML:
```yaml
command: "sh interface | include Queueing strategy:"
```

####Комбинация элементов
Словарь, в котором есть два ключа access и trunk. Значения, которые соответствуют этим ключам - списки команд:
```yaml
access:
- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable

trunk:
- switchport trunk encapsulation dot1q
- switchport mode trunk
- switchport trunk native vlan 999
- switchport trunk allowed vlan
```

Список словарей:
```yaml
- BS: 1550
  IT: 791
  id: 11
  name: Liverpool
  to_id: 1
  to_name: LONDON
- BS: 1510
  IT: 793
  id: 12
  name: Bristol
  to_id: 1
  to_name: LONDON
- BS: 1650
  IT: 892
  id: 14
  name: Coventry
  to_id: 2
  to_name: Manchester
```

### Модуль PyYAML
Для работы с YAML в Python используется модуль PyYAML.
Он не входит в стандартную библиотеку модулей, поэтому его нужно установить:
```
pip install pyyaml
```

Работа с ним аналогична модулям csv и json.

####Чтение из YAML

Попробуем преобразовать данные из файла YAML в объекты Python.

Файл info.yaml:
```yaml
- BS: 1550
  IT: 791
  id: 11
  name: Liverpool
  to_id: 1
  to_name: LONDON
- BS: 1510
  IT: 793
  id: 12
  name: Bristol
  to_id: 1
  to_name: LONDON
- BS: 1650
  IT: 892
  id: 14
  name: Coventry
  to_id: 2
  to_name: Manchester
```

Чтение из YAML выполняется очень просто:
```python
In [1]: import yaml

In [2]: templates = yaml.load(open('info.yaml'))

In [3]: templates
Out[3]:
[{'BS': 1550,
  'IT': 791,
  'id': 11,
  'name': 'Liverpool',
  'to_id': 1,
  'to_name': 'LONDON'},
 {'BS': 1510,
  'IT': 793,
  'id': 12,
  'name': 'Bristol',
  'to_id': 1,
  'to_name': 'LONDON'},
 {'BS': 1650,
  'IT': 892,
  'id': 14,
  'name': 'Coventry',
  'to_id': 2,
  'to_name': 'Manchester'}]
```

Формат YAML очень удобен для хранения различных параметров. Особенно, если вы их заполняете вручную, а не берете из какого-то источника.

И, как минимум, YAML пригодится нам для работы с Ansible.



####Запись в YAML
Попробуем записать объекты Python в YAML (файл yaml_write.py):
```python
import yaml

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']


access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_yaml = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.yaml', 'w') as f:
    f.write(yaml.dump(to_yaml))

with open('sw_templates.yaml') as f:
    print f.read()

```

Файл sw_templates.yaml выглядит таким образом:
```yaml
access: [switchport mode access, switchport access vlan, switchport nonegotiate, spanning-tree
    portfast, spanning-tree bpduguard enable]
trunk: [switchport trunk encapsulation dot1q, switchport mode trunk, switchport trunk
    native vlan 999, switchport trunk allowed vlan]
```

То есть, по умолчанию, список записался в одну строку. Но удобнее, когда каждый элемент списка находится в одной строке.

Для того, чтобы изменить формат записи, добавляем параметр ```default_flow_style=False``` (файл yaml_write_ver2.py):
```python
import yaml

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']


access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_yaml = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.yaml', 'w') as f:
    f.write(yaml.dump(to_yaml, default_flow_style=False))

with open('sw_templates.yaml') as f:
    print f.read()
```

Теперь содержимое файла sw_templates.yaml выглядит таким образом:
```yaml
access:
- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable
trunk:
- switchport trunk encapsulation dot1q
- switchport mode trunk
- switchport trunk native vlan 999
- switchport trunk allowed vlan
```

