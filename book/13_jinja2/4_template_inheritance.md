{% raw %}
## Наследование шаблонов

Наследование шаблонов это очень мощный функционал, который позволяет избежать повторения одного и того же в разных шаблонов.

При использовании наследования различают:
* __базовый шаблон__ - это шаблон, в котором описывается каркас шаблона.
 * в этом шаблоне могут находится любые обычные выражения или текст. Но, кроме того, в этом шаблоне определяются специальные __блоки (block)__. 
* __дочерний шаблон__ - шаблон, который расширяет базовый шаблон, заполняя обозначенные блоки.
 * дочерние шаблоны могут переписывать или дополнять блоки, определенные в базовом шаблоне.


Пример базового шаблона templates/base_router.txt:
```
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
{% block ospf %}
router ospf 1
 auto-cost reference-bandwidth 10000
{% endblock %}
!
{% block bgp %}
{% endblock %}
!
{% block alias %}
{% endblock %}
!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!
```

Обратите внимание на три блока, которые созданы в шаблоне:
```
{% block ospf %}
router ospf 1
 auto-cost reference-bandwidth 10000
{% endblock %}
!
{% block bgp %}
{% endblock %}
!
{% block alias %}
{% endblock %}
```

Это заготовки для соответствующих разделов конфигурации.
Дочерний шаблон, который будет использовать этот базовый шаблон как основу, может заполнять все блоки или только какие-то из них.


Дочерний шаблон templates/hq_router.txt:
```
{% extends "base_router.txt" %}

{% block ospf %}
{{ super() }}
{% for networks in ospf %}
 network {{ networks.network }} area {{ networks.area }}
{% endfor %}
{% endblock %}

{% block alias %}
alias configure sh do sh
alias exec ospf sh run | s ^router ospf
alias exec bri show ip int bri | exc unass
alias exec id show int desc
alias exec top sh proc cpu sorted | excl 0.00%__0.00%__0.00%
alias exec c conf t
alias exec diff sh archive config differences nvram:startup-config system:running-config
alias exec desc sh int desc | ex down
{% endblock %}
```

Первая строка в шаблоне templates/hq_router.txt очень важна:
```
{% extends "base_router.txt" %}
```

Именно она говорит о том, что шаблон hq_router.txt будет построен на основе шаблона base_router.txt.

Внутри дочернего шаблона всё происходит внутри блоков.
Засчет блоков, которые были определены в базовом шаблоне, мы расширяем его, внутри дочернего.

> Обратите внимание, что если вы допишите в дочернем шаблоне (templates/hq_router.txt) строки за пределами блоков, они не будут учитываться.

В базовом шаблоне было три блока: ospf, bgp, alias.
В дочернем шаблоне мы заполняем только два из них: ospf и alias.

В этом удобство наследования. Мы не обязаны заполнять все блоки в каждом дочернем шаблоне.

При этом, блоки ospf и alias мы используем по-разному.
В базовом шаблоне, в блоке ospf уже была часть конфигурации:
```
{% block ospf %}
router ospf 1
 auto-cost reference-bandwidth 10000
{% endblock %}
```

Поэтому, в дочернем шаблоне у нас есть выбор: использовать эту конфигурацию и дополнить её, или полностью переписать всё в дочернем шаблоне.

В данном случае, мы выбрали дополнять.
Именно поэтому в дочернем шаблоне templates/hq_router.txt блок ospf начинается с выражения ```{{ super() }}```:
```
{% block ospf %}
{{ super() }}
{% for networks in ospf %}
 network {{ networks.network }} area {{ networks.area }}
{% endfor %}
{% endblock %}
```

super переносит в дочерний шаблон содержимое этого блока из родительского шаблона.
Засчет этого, в дочерний шаблон перенесутся строки из родительского.

> Выражение super не обязательно должно находится в самом начале блока. Оно может быть в любом месте блока. Содержимое базового шаблона, перенесется в то место, где находится выражение super.

В блоке alias мы просто пишем нужные alias.
И, даже если бы в родительском шаблоне были какие-то настроки, они были бы затерты содержимым дочернего шаблона.

Файл с данными для генерации конфигурации по шаблону (data_files/hq_router.yml):
```json
ospf:
  - network: 10.0.1.0 0.0.0.255
    area: 0
  - network: 10.0.2.0 0.0.0.255
    area: 2
  - network: 10.1.1.0 0.0.0.255
    area: 0
```

Результат выполнения будет таким:
```
$ python cfg_gen.py templates/hq_router.txt data_files/hq_router.yml
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
router ospf 1
 auto-cost reference-bandwidth 10000

 network 10.0.1.0 0.0.0.255 area 0
 network 10.0.2.0 0.0.0.255 area 2
 network 10.1.1.0 0.0.0.255 area 0
!
!
alias configure sh do sh
alias exec ospf sh run | s ^router ospf
alias exec bri show ip int bri | exc unass
alias exec id show int desc
alias exec top sh proc cpu sorted | excl 0.00%__0.00%__0.00%
alias exec c conf t
alias exec diff sh archive config differences nvram:startup-config system:running-config
alias exec desc sh int desc | ex down
!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!
```

Обратите внимание, что в блоке ospf есть и команды из базового шаблона, и команды из дочернего шаблона.

Мы рассмотрели основные возможности Jinja2.
Но на этом они не заканчиваются.
В остальном, вам поможет [документация](http://jinja.pocoo.org/docs/dev/).

{% endraw %}
