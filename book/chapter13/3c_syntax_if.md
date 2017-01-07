##  if/elif/else

if позволяет добавлять условие в шаблон. Например, можно использовать if чтобы добавлять какие-то части шаблона, в зависимости от наличия переменных в словаре с данными.

Пример шаблона templates/if.txt:
```
hostname {{ name }}

interface Loopback0
 ip address 10.0.0.{{ id }} 255.255.255.255

{% for vlan, name in vlans.iteritems() %}
vlan {{ vlan }}
 name {{ name }}
{% endfor %}

{% if ospf %}
router ospf 1
 router-id 10.0.0.{{ id }}
 auto-cost reference-bandwidth 10000
{% for networks in ospf %}
 network {{ networks.network }} area {{ networks.area }}
{% endfor %}
{% endif %}
```

Выражение ```if ospf``` работает так же, как в Python: если переменная существует и не пустая, результат будет True. Если переменной нет, или они пустая, результат будет False.

То есть, в этом шаблоне конфигурация OSPF генерируется только в том случае, если мы передали переменную ospf с какими-то значениями внутри.

Мы попробуем сгенерировать конфигурацию с двумя вариантами данных.
Сначала, с файлом data_files/if.yml, в котором нет переменной ospf:
```yml
id: 3
name: R3
vlans:
  10: Marketing
  20: Voice
  30: Management
```

Результат будет таким:
```
$ python cfg_gen.py templates/if.txt data_files/if.yml

hostname R3

interface Loopback0
 ip address 10.0.0.3 255.255.255.255

vlan 10
 name Marketing
vlan 20
 name Voice
vlan 30
 name Management

```


Теперь аналогичный шаблон, но с файлом data_files/if_ospf.yml:
```yml
id: 3
name: R3
vlans:
  10: Marketing
  20: Voice
  30: Management
ospf:
  - network: 10.0.1.0 0.0.0.255
    area: 0
  - network: 10.0.2.0 0.0.0.255
    area: 2
  - network: 10.1.1.0 0.0.0.255
    area: 0
```

Теперь результат выполнения будет таким:
```
hostname R3

interface Loopback0
 ip address 10.0.0.3 255.255.255.255

vlan 10
 name Marketing
vlan 20
 name Voice
vlan 30
 name Management

router ospf 1
 router-id 10.0.0.3
 auto-cost reference-bandwidth 10000
 network 10.0.1.0 0.0.0.255 area 0
 network 10.0.2.0 0.0.0.255 area 2
 network 10.1.1.0 0.0.0.255 area 0
```

