## Примеры использования TextFSM

В этом разделе мы посмотрим на несколько более сложных примеров шаблонов и использования TextFSM.


В этом разделе мы будем использовать скрипт parse_output.py, который не привязан к конкретному шаблону и выводу: шаблон и вывод команды будут передаваться как параметры:
```python
import sys
import textfsm
from tabulate import tabulate

template = sys.argv[1]
output_file = sys.argv[2]

f = open(template)
output = open(output_file).read()

re_table = textfsm.TextFSM(f)

header = re_table.header
result = re_table.ParseText(output)

print tabulate(result, headers=header)

```

Запускать скрипт мы будем таким образом:
```
python parse_output.py template command_output
```

> Модуль tabulate используется для отображения данных в табличном виде (его нужно установить, если хотите использовать этот скрипт).

Обработка данных по шаблону всегда выполняется одинаково. Поэтому скрипт будет одинаковый и только шаблон и данные отличаться. Начиная с простого примера, разберемся с тем как использовать TextFSM.

### show clock

Разберемся с простым примером, вывод команды sh clock:
```
15:10:44.867 UTC Sun Nov 13 2016
```

Для начала, в шаблоне надо определить переменные:
* В начале каждой строки должно быть ключевое слово Value
 * каждая переменная определяет столбец в таблице
* следующее слово - название переменной
* после названия, в скобках, регулярное выражение, которое описывает значение переменной

Определение переменных выглядит так:
```
Value Time (..:..:..)
Value Timezone (\S+)
Value WeekDay (\w+)
Value Month (\w+)
Value MonthDay (\d+)
Value Year (\d+)
```

На всякий случай, подсказка по спецсимволам:
* ```.``` - любой символ
* ```+``` - одно или более повторений предыдущего символа
* ```\S``` - все символы, кроме whitespace
* ```\w``` - любая буква или цифра
* ```\d``` - любая цифра

После определения переменных, должна идти пустая строка и состояние __Start__, а после, начиная с пробела и символа ```^```, идет правило:
```
Value Time (..:..:..)
Value Timezone (\S+)
Value WeekDay (\w+)
Value Month (\w+)
Value MonthDay (\d+)
Value Year (\d+)

Start
  ^${Time}.* ${Timezone} ${WeekDay} ${Month} ${MonthDay} ${Year} -> Record
```

> Так как, в данном случае, в выводе всего одна строка, можно не писать в шаблоне действие Record. Но лучше его использовать в таких ситуациях, когда надо записать значения, чтобы привыкать к этому синтаксу и не ошибиться, когда нужна обработка нескольких строк.

Когда TextFSM обрабатывает строки вывода, он подставляет вместо переменных, их значения. В итоге правило будет выглядеть так:
```
^(..:..:..).* (\S+) (\w+) (\w+) (\d+) (\d+)
```

Когда это регулярное выражение применяется в выводу show clock, в каждой группе регулярного выражения, будет находится соответствующее значение:
* 1 группа: 15:10:44
* 2 группа: UTC
* 3 группа: Sun
* 4 группа: Nov
* 5 группа: 13
* 6 группа: 2016

В правиле, кроме явного действия Record, которое указывает, что запись надо поместить в финальную таблицу, по умолчанию также используется правило Next, которое указывает, что надо перейти к следующей строке текста. Но так как в выводе команды sh clock, только одна строка, обработка завершается.

Результат отработки скрипта будет таким:
```
$ python parse_output.py sh_clock.template show_clock.txt
Time      Timezone    WeekDay    Month      MonthDay    Year
--------  ----------  ---------  -------  ----------  ------
15:10:44  UTC         Sun        Nov              13    2016
```

### show cdp neighbors detail

Теперь попробуем обработать вывод команды show cdp neighbors detail. Особенность этой команды в том, что нужные нам данные находятся не в одной строке, а в разных.

В файле cdp_detail_output.txt находится вывод команды show cdp neighbors detail:
```
SW1#show cdp neighbors detail
-------------------------
Device ID: SW2
Entry address(es):
  IP address: 10.1.1.2
Platform: cisco WS-C2960-8TC-L,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/0/16,  Port ID (outgoing port): GigabitEthernet0/1
Holdtime : 164 sec

Version :
Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Mon 03-Mar-14 22:53 by prod_rel_team

advertisement version: 2
VTP Management Domain: ''
Native VLAN: 1
Duplex: full
Management address(es):
  IP address: 10.1.1.2

-------------------------
Device ID: R1
Entry address(es):
  IP address: 10.1.1.1
Platform: Cisco 3825,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/0/22,  Port ID (outgoing port): GigabitEthernet0/0
Holdtime : 156 sec

Version :
Cisco IOS Software, 3800 Software (C3825-ADVENTERPRISEK9-M), Version 12.4(24)T1, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2009 by Cisco Systems, Inc.
Compiled Fri 19-Jun-09 18:40 by prod_rel_team

advertisement version: 2
VTP Management Domain: ''
Duplex: full
Management address(es):

-------------------------
Device ID: R2
Entry address(es):
  IP address: 10.2.2.2
Platform: Cisco 2911,  Capabilities: Router Switch IGMP
Interface: GigabitEthernet1/0/21,  Port ID (outgoing port): GigabitEthernet0/0
Holdtime : 156 sec

Version :
Cisco IOS Software, 2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2009 by Cisco Systems, Inc.
Compiled Fri 19-Jun-09 18:40 by prod_rel_team

advertisement version: 2
VTP Management Domain: ''
Duplex: full
Management address(es):

```

Попробуем получить из вывода такие поля:
* LOCAL_HOST - имя устройства, которое мы получим из приглашения
* DEST_HOST - имя соседа
* MGMNT_IP - IP-адрес соседа
* PLATFORM - модель соседнего устройства
* LOCAL_PORT - локальный интерфейс, который соединен с соседом
* REMOTE_PORT - порт соседнего устройства
* IOS_VERSION - версия IOS соседа

Шаблон выглядит таким образом:
```
Value LOCAL_HOST (\S+)
Value DEST_HOST (\S+)
Value MGMNT_IP (.*)
Value PLATFORM (.*)
Value LOCAL_PORT (.*)
Value REMOTE_PORT (.*)
Value IOS_VERSION (\S+)

Start
  ^${LOCAL_HOST}[>#].
  ^Device ID: ${DEST_HOST}
  ^.*IP address: ${MGMNT_IP}
  ^Platform: ${PLATFORM},
  ^Interface: ${LOCAL_PORT},  Port ID \(outgoing port\): ${REMOTE_PORT}
  ^.*Version ${IOS_VERSION},
```

Попробуем запустить скрипт:
```
$ python parse_output.py show_cdp_neighbors_detail.template cdp_detail_output.txt
LOCAL_HOST    DEST_HOST    MGMNT_IP    PLATFORM    LOCAL_PORT             REMOTE_PORT         IOS_VERSION
------------  -----------  ----------  ----------  ---------------------  ------------------  -------------
SW1           R2           10.2.2.2    Cisco 2911  GigabitEthernet1/0/21  GigabitEthernet0/0  15.2(2)T1
```

Несмотря на то, что правила с переменными описаны в разных строках, и, соответственно, работают с разными строками, TextFSM собирает их в одну строку таблицы.
То есть, переменные, которые мы определяем в начале шаблона, задают строку итоговой таблицы.

Обратите внимание, что в файле cdp_detail_output.txt находится вывод с тремя соседями, а в таблице только один сосед, последний.

#### Record
Так получилось из-за того, что в шаблоне не указано действие __Record__.
И в итоге, в финальной таблице осталась только последняя строка.

Если мы исправим шаблон таким образом:
```
Value LOCAL_HOST (\S+)
Value DEST_HOST (\S+)
Value MGMNT_IP (.*)
Value PLATFORM (.*)
Value LOCAL_PORT (.*)
Value REMOTE_PORT (.*)
Value IOS_VERSION (\S+)

Start
  ^${LOCAL_HOST}[>#].
  ^Device ID: ${DEST_HOST}
  ^.*IP address: ${MGMNT_IP}
  ^Platform: ${PLATFORM},
  ^Interface: ${LOCAL_PORT},  Port ID \(outgoing port\): ${REMOTE_PORT}
  ^.*Version ${IOS_VERSION}, -> Record
```

То, запустив скрипт еще раз, мы получим такой результат:
```
$ python parse_output.py show_cdp_neighbors_detail.template cdp_detail_output.txt
LOCAL_HOST    DEST_HOST    MGMNT_IP    PLATFORM              LOCAL_PORT             REMOTE_PORT         IOS_VERSION
------------  -----------  ----------  --------------------  ---------------------  ------------------  -------------
SW1           SW2          10.1.1.2    cisco WS-C2960-8TC-L  GigabitEthernet1/0/16  GigabitEthernet0/1  12.2(55)SE9
              R1           10.1.1.1    Cisco 3825            GigabitEthernet1/0/22  GigabitEthernet0/0  12.4(24)T1
              R2           10.2.2.2    Cisco 2911            GigabitEthernet1/0/21  GigabitEthernet0/0  15.2(2)T1
```

Теперь мы получили вывод со всех трёх устройств.
Но, переменная LOCAL_HOST отображается не в каждой строке, а только в первой.

#### Filldown
Связано это с тем, что приглашение, из которого мы взяли значение переменной, появляется только один раз. И, для того, чтобы оно появлялось и в последующих строках, надо использовать действие __Filldown__ для переменной LOCAL_HOST:
```
Value Filldown LOCAL_HOST (\S+)
Value DEST_HOST (\S+)
Value MGMNT_IP (.*)
Value PLATFORM (.*)
Value LOCAL_PORT (.*)
Value REMOTE_PORT (.*)
Value IOS_VERSION (\S+)

Start
  ^${LOCAL_HOST}[>#].
  ^Device ID: ${DEST_HOST}
  ^.*IP address: ${MGMNT_IP}
  ^Platform: ${PLATFORM},
  ^Interface: ${LOCAL_PORT},  Port ID \(outgoing port\): ${REMOTE_PORT}
  ^.*Version ${IOS_VERSION}, -> Record
```

Теперь мы получили такой вывод:
```
$ python parse_output.py show_cdp_neighbors_detail.template cdp_detail_output.txt
LOCAL_HOST    DEST_HOST    MGMNT_IP    PLATFORM              LOCAL_PORT             REMOTE_PORT         IOS_VERSION
------------  -----------  ----------  --------------------  ---------------------  ------------------  -------------
SW1           SW2          10.1.1.2    cisco WS-C2960-8TC-L  GigabitEthernet1/0/16  GigabitEthernet0/1  12.2(55)SE9
SW1           R1           10.1.1.1    Cisco 3825            GigabitEthernet1/0/22  GigabitEthernet0/0  12.4(24)T1
SW1           R2           10.2.2.2    Cisco 2911            GigabitEthernet1/0/21  GigabitEthernet0/0  15.2(2)T1
SW1
```

Теперь значение переменной LOCAL_HOST появилось во всех трёх строках. Но появился ещё один странный эффект - последняя строка, в которой заполнена только колонка LOCAL_HOST.

#### Required
Дело в том, что все переменные, которые мы определили, опциональны. И, к тому же, одна переменная с параметром Filldown. И, чтобы избавиться от последней строки, нужна указать одну переменную обязательной, с помощью параметра __Required__:
```
Value Filldown LOCAL_HOST (\S+)
Value Required DEST_HOST (\S+)
Value MGMNT_IP (.*)
Value PLATFORM (.*)
Value LOCAL_PORT (.*)
Value REMOTE_PORT (.*)
Value IOS_VERSION (\S+)

Start
  ^${LOCAL_HOST}[>#].
  ^Device ID: ${DEST_HOST}
  ^.*IP address: ${MGMNT_IP}
  ^Platform: ${PLATFORM},
  ^Interface: ${LOCAL_PORT},  Port ID \(outgoing port\): ${REMOTE_PORT}
  ^.*Version ${IOS_VERSION}, -> Record
```

Теперь мы получим корректный вывод:
```
$ python parse_output.py show_cdp_neighbors_detail.template cdp_detail_output.txt
LOCAL_HOST    DEST_HOST    MGMNT_IP    PLATFORM              LOCAL_PORT             REMOTE_PORT         IOS_VERSION
------------  -----------  ----------  --------------------  ---------------------  ------------------  -------------
SW1           SW2          10.1.1.2    cisco WS-C2960-8TC-L  GigabitEthernet1/0/16  GigabitEthernet0/1  12.2(55)SE9
SW1           R1           10.1.1.1    Cisco 3825            GigabitEthernet1/0/22  GigabitEthernet0/0  12.4(24)T1
SW1           R2           10.2.2.2    Cisco 2911            GigabitEthernet1/0/21  GigabitEthernet0/0  15.2(2)T1
```

### show ip interface brief

В случае, когда нужно обработать данные, которые выведены столбцами, шаблон TextFSM, наиболее удобен. Посмотрим на шаблон для вывода команды show ip interface brief:
```
Value INT (\S+)
Value ADDR (\S+)
Value STATUS (up|down|administratively down)
Value PROTO (up|down)

Start
  ^${INTF}\s+${ADDR}\s+\w+\s+\w+\s+${STATUS}\s+${PROTO} -> Record
```

В этом случае, правило можно описать одной строкой.

Посмотрим на результат применения шаблона к такому выводу:
```
R1#show ip interface brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            15.0.15.1       YES manual up                    up
FastEthernet0/1            10.0.12.1       YES manual up                    up
FastEthernet0/2            10.0.13.1       YES manual up                    up
FastEthernet0/3            unassigned      YES unset  up                    up
Loopback0                  10.1.1.1        YES manual up                    up
Loopback100                100.0.0.1       YES manual up                    up
```

Результат выполнения будет таким:
```
$ python parse_output.py templates/cisco_ios_show_ip_int_brief.template show_ip_int_br.txt
INT              ADDR        STATUS    PROTO
---------------  ----------  --------  -------
FastEthernet0/0  15.0.15.1   up        up
FastEthernet0/1  10.0.12.1   up        up
FastEthernet0/2  10.0.13.1   up        up
FastEthernet0/3  unassigned  up        up
Loopback0        10.1.1.1    up        up
Loopback100      100.0.0.1   up        up
```

### show ip route ospf

Рассмотрим случай, когда нам нужно обработать вывод команды show ip route ospf и в таблице маршрутизации есть несколько маршрутов к одной сети.

Допустим, что в таком случае, мы хотим получить для маршрутов к одной сети, вместо нескольких строк, где будет повторяться сеть, одну запись, в которой все доступные next-hop адреса собраны в список.

Пример вывода команды show ip route ospf:
```
R1#sh ip route ospf
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 10 subnets, 2 masks
O        10.0.24.0/24 [110/20] via 10.0.12.2, 1w2d, Ethernet0/1
O        10.0.34.0/24 [110/20] via 10.0.13.3, 1w2d, Ethernet0/2
O        10.2.2.2/32 [110/11] via 10.0.12.2, 1w2d, Ethernet0/1
O        10.3.3.3/32 [110/11] via 10.0.13.3, 1w2d, Ethernet0/2
O        10.4.4.4/32 [110/21] via 10.0.13.3, 1w2d, Ethernet0/2
                     [110/21] via 10.0.12.2, 1w2d, Ethernet0/1
                     [110/21] via 10.0.14.4, 1w2d, Ethernet0/3
O        10.5.35.0/24 [110/20] via 10.0.13.3, 1w2d, Ethernet0/2
```

> Для этого примера мы упрощаем задачу и считаем, что маршруты могут быть только OSPF и с обозначением, только O (то есть, только внутризональные маршруты).

Шаблон может выглядеть так:
```
Value Network (([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}))
Value Mask (\/\d{1,2})
Value Distance (\d+)
Value Metric (\d+)
Value NextHop ([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})

Start
  ^O +${Network}${Mask}\s\[${Distance}\/${Metric}\]\svia\s${NextHop}, -> Record
```

Результат получился такой:
```
Network    Mask      Distance    Metric  NextHop
---------  ------  ----------  --------  ---------
10.0.24.0  /24            110        20  10.0.12.2
10.0.34.0  /24            110        20  10.0.13.3
10.2.2.2   /32            110        11  10.0.12.2
10.3.3.3   /32            110        11  10.0.13.3
10.4.4.4   /32            110        21  10.0.13.3
10.5.35.0  /24            110        20  10.0.13.3
```

Всё нормально, но только вот потерялись варианты путей для маршрута 10.4.4.4/32. Это логично, ведь мы не написали правило, которое подошло бы для такой строки.

#### List

Воспользуемся опцией __List__ для переменной NextHop:
```
Value Network (([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}))
Value Mask (\/\d{1,2})
Value Distance (\d+)
Value Metric (\d+)
Value List NextHop ([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})

Start
  ^O +${Network}${Mask}\s\[${Distance}\/${Metric}\]\svia\s${NextHop}, -> Record
```

Теперь вывод получился таким:
```
Network    Mask      Distance    Metric  NextHop
---------  ------  ----------  --------  -------------
10.0.24.0  /24            110        20  ['10.0.12.2']
10.0.34.0  /24            110        20  ['10.0.13.3']
10.2.2.2   /32            110        11  ['10.0.12.2']
10.3.3.3   /32            110        11  ['10.0.13.3']
10.4.4.4   /32            110        21  ['10.0.13.3']
10.5.35.0  /24            110        20  ['10.0.13.3']
```

Изменилось то, что теперь в столбце NextHop отображается список, но пока с одним элементом.

Теперь надо сделать несколько изменений в шаблоне.

Надо перенести действие __Record__. Так как, перед записью маршрута, для которого есть несколько путей, надо добавить к нему все доступные адреса NextHop.

Для этого запись перенесем на момент, когда встречается следующая строка с маршрутом. Но в этот момент нам надо записать предыдущую строку и только после этого, уже записывать текущую. Для этого, мы используем такую запись:
```
  ^O -> Continue.Record
```

В ней действие __Record__ говорит, что надо записать текущее значение переменных. А так как в этом правиле переменных нет, то записывается то, что было в предыдущих значениях. Действие __Continue__ говорит, что надо продолжить работать с текущей строкой так, как-будто совпадения не было. Засчет этого, сработает слудующая строка.

Остается добавить правило, которое будет описывать дополнительные маршруты к сети (в них нет сети и маски):
```
  ^\s+\[${Distance}\/${Metric}\]\svia\s${NextHop},
```


Итоговый шаблон выглядит так:
```
Value Network (([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}))
Value Mask (\/\d{1,2})
Value Distance (\d+)
Value Metric (\d+)
Value List NextHop ([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})

Start
  ^O -> Continue.Record
  ^O +${Network}${Mask}\s\[${Distance}\/${Metric}\]\svia\s${NextHop},
  ^\s+\[${Distance}\/${Metric}\]\svia\s${NextHop},
```

> Этот пример сложнее предыдущих, чтобы его лучше понять, попробуйте постепенно перейти с прошлого варианта шаблона, к последнему.

В результате, мы получим такой вывод:
```
Network    Mask      Distance    Metric  NextHop
---------  ------  ----------  --------  ---------------------------------------
10.0.24.0  /24            110        20  ['10.0.12.2']
10.0.34.0  /24            110        20  ['10.0.13.3']
10.2.2.2   /32            110        11  ['10.0.12.2']
10.3.3.3   /32            110        11  ['10.0.13.3']
10.4.4.4   /32            110        21  ['10.0.13.3', '10.0.12.2', '10.0.14.4']
10.5.35.0  /24            110        20  ['10.0.13.3']
```

На этом мы заканчиваем разбираться с шаблонами. Примеры шаблонов для Cisco и другого оборудования можно посмотреть в проекте [ntc-ansible](https://github.com/networktocode/ntc-templates/tree/89c57342b47c9990f0708226fb3f268c6b8c1549/templates).
