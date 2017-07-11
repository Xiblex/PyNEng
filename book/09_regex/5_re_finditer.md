### ```re.finditer()```

Функция ```finditer()```:
* используется для поиска всех непересекающихся совпадений в шаблоне
* возвращает итератор с объектами Match

Функция finditer отлично подходит для обработки тех команд, вывод которых отображается столбцами.
Например, sh ip int br, sh mac address-table и др.
В этом случае, его можно применять ко всему выводу команды.

Например, лог-файл, который разбирался с помощью search и match, можно разобрать и с помощью finditer.

В этом случае, вывод можно не перебирать построчно, а передать все содержимое файла: 
```python
import re

regex = ('Host \S+ '
         'in vlan (\d+) '
         'is flapping between port '
         '(\S+) and port (\S+)')

ports = set()

with open('log.txt') as f:
    match = re.finditer(regex, f.read())
    for m in match:
        vlan = m.group(1)
        ports.add(m.group(2))
        ports.add(m.group(3))

print('Петля между портами {} в VLAN {}'.format(', '.join(ports), vlan))

```


Вывод будет таким же:
```
$ python re_finditer.py
Петля между портами Gi0/19, Gi0/24, Gi0/16 в VLAN 10
```

### Обработка вывода show cdp neighbors detail

С помощью finditer можно обработать вывод sh cdp neighbors detail, так же, как и в подразделе re.search.

Скрипт почти полностью аналогичен варианту с re.search (файл parse_sh_cdp_neighbors_detail_finditer.py):
```python
import re
from pprint import pprint


def parse_cdp(filename):
    regex = ('Device ID: (?P<device>\S+)'
             '|IP address: (?P<ip>\S+)'
             '|Platform: (?P<platform>\S+ \S+),'
             '|Cisco IOS Software, (?P<ios>.+), RELEASE')

    result = {}

    with open('sh_cdp_neighbors_sw1.txt') as f:
        match_iter = re.finditer(regex, f.read())
        for match in match_iter:
            if match.lastgroup == 'device':
                device = match.group(match.lastgroup)
                result[device] = {}
            elif device:
                result[device][match.lastgroup] = match.group(match.lastgroup)

    return result

pprint(parse_cdp('sh_cdp_neighbors_sw1.txt'))

```

Теперь совпадения ищутся во всем файле, а не в каждой строке отдельно:
```python
    with open('sh_cdp_neighbors_sw1.txt') as f:
        match_iter = re.finditer(regex, f.read())
```

Затем перебираются совпадения:
```python
    with open('sh_cdp_neighbors_sw1.txt') as f:
        match_iter = re.finditer(regex, f.read())
        for match in match_iter:

```

Остальное аналогично.

Результат будет таким:
```python
$ python parse_sh_cdp_neighbors_detail_finditer.py
{'R1': {'ios': '3800 Software (C3825-ADVENTERPRISEK9-M), Version 12.4(24)T1',
        'ip': '10.1.1.1',
        'platform': 'Cisco 3825'},
 'R2': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.2.2.2',
        'platform': 'Cisco 2911'},
 'SW2': {'ios': 'C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9',
         'ip': '10.1.1.2',
         'platform': 'cisco WS-C2960-8TC-L'}}

```

Хотя результат аналогичный, с finditer больше возможностей, так как можно указывать не только то, что должно находится в нужной строке, но и в строках вокруг.

Например, можно точнее указать какой именно IP-адрес надо взять:
```
Device ID: SW2
Entry address(es):
  IP address: 10.1.1.2
Platform: cisco WS-C2960-8TC-L,  Capabilities: Switch IGMP

...

Native VLAN: 1
Duplex: full
Management address(es):
  IP address: 10.1.1.2
```

Например, если нужно взять первый IP-адрес, можно так дополнить регулярное выражение:
```python
regex = ('Device ID: (?P<device>\S+)'
         '|Entry address.*\n +IP address: (?P<ip>\S+)'
         '|Platform: (?P<platform>\S+ \S+),'
         '|Cisco IOS Software, (?P<ios>.+), RELEASE')
```

