## Модуль ios_command

Модуль ios_command - отправляет команду на устройство под управлением IOS и возвращает результат выполнения команды.

> **Note** Модуль ios_command не поддерживает отправку команд в конфигурационном режиме.
> Для этого используется отдельный модуль - ios_config.

Когда мы отправляем команду на устройство, модуль самостоятельно аутентифицируется по SSH, переходит в режим enable и дает команду ```terminal length 0```, чтобы вывод команд show отражался полностью, а не постранично.

Посмотрим на простой пример использования модуля ios_command (playbook 4_ios_command.yml):
```
---

- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: run sh ip int br
      ios_command:
        commands: show ip int br
        provider: "{{ cli }}"
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug: var=sh_ip_int_br_result.stdout_lines
```

Модуль ios_command ожидает параметры:
* commands - список команд, которые нужно отправить на устройство
* provider - словарь с параметрами подключения
 * в нашем случае, он указан в файле group_vars/all.yml

> **Caution** Обратите внимание, что параметр register находится на одном уровне с именем задачи и модулем, а не на уровне параметров модуля ios_command.

Попробуем запустить playbook:
```
$ ansible-playbook 2_ios_command.yml
SSH password:

PLAY [Run show commands on routers] ********************************************

TASK [run sh ip int br] ********************************************************
ok: [192.168.100.1]
ok: [192.168.100.2]
ok: [192.168.100.3]

TASK [Debug registered var] ****************************************************
ok: [192.168.100.1] => {
    "sh_ip_int_br_result.stdout_lines": [
        [
            "Interface                  IP-Address      OK? Method Status                Protocol",
            "Ethernet0/0                192.168.100.1   YES NVRAM  up                    up      ",
            "Ethernet0/1                192.168.200.1   YES NVRAM  up                    up      ",
            "Ethernet0/2                unassigned      YES NVRAM  administratively down down    ",
            "Ethernet0/3                unassigned      YES NVRAM  administratively down down    ",
            "Loopback0                  10.1.1.1        YES manual up                    up      "
        ]
    ]
}
ok: [192.168.100.2] => {
    "sh_ip_int_br_result.stdout_lines": [
        [
            "Interface                  IP-Address      OK? Method Status                Protocol",
            "Ethernet0/0                192.168.100.2   YES manual up                    up      ",
            "Ethernet0/1                unassigned      YES unset  administratively down down    ",
            "Ethernet0/2                unassigned      YES unset  administratively down down    ",
            "Ethernet0/3                unassigned      YES unset  administratively down down    ",
            "Loopback0                  10.1.1.1        YES manual up                    up      "
        ]
    ]
}
ok: [192.168.100.3] => {
    "sh_ip_int_br_result.stdout_lines": [
        [
            "Interface                  IP-Address      OK? Method Status                Protocol",
            "Ethernet0/0                192.168.100.3   YES manual up                    up      ",
            "Ethernet0/1                unassigned      YES unset  administratively down down    ",
            "Ethernet0/2                unassigned      YES unset  administratively down down    ",
            "Ethernet0/3                unassigned      YES unset  administratively down down    ",
            "Loopback0                  10.1.1.1        YES manual up                    up      "
        ]
    ]
}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=2    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=2    changed=0    unreachable=0    failed=0
```

В отличии от использования модуля raw, когда мы используем модуль ios_command, playbook не указывает, что были выполнены изменения.


### Выполнение нескольких команд

Модуль ios_command позволяет выполнять несколько команд.
Попробуем выполнить несколько команд и получить их вывод.

Playbook 4a_ios_command.yml:
```
---

- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: run show commands
      ios_command:
        commands:
          - show ip int br
          - sh ip route
        provider: "{{ cli }}"
      register: show_result

    - name: Debug registered var
      debug: var=show_result.stdout_lines
```

Теперь мы указываем две команды, в модуле ios_command, поэтому синтаксис должен быть немного другим - команды должны быть указаны, как список в формате YAML.


Посмотрим на результат выполнения playbook:
```
$ ansible-playbook 2a_ios_command.yml
SSH password:

PLAY [Run show commands on routers] ********************************************

TASK [run show commands] *******************************************************
ok: [192.168.100.1]
ok: [192.168.100.3]
ok: [192.168.100.2]

TASK [Debug registered var] ****************************************************
ok: [192.168.100.1] => {
    "show_result.stdout_lines": [
        [
            "Interface                  IP-Address      OK? Method Status                Protocol",
            "Ethernet0/0                192.168.100.1   YES NVRAM  up                    up      ",
            "Ethernet0/1                192.168.200.1   YES NVRAM  up                    up      ",
            "Ethernet0/2                unassigned      YES NVRAM  administratively down down    ",
            "Ethernet0/3                unassigned      YES NVRAM  administratively down down    ",
            "Loopback0                  10.1.1.1        YES manual up                    up      "
        ],
        [
            "Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP",
            "       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area ",
            "       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2",
            "       E1 - OSPF external type 1, E2 - OSPF external type 2",
            "       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2",
            "       ia - IS-IS inter area, * - candidate default, U - per-user static route",
            "       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP",
            "       + - replicated route, % - next hop override",
            "",
            "Gateway of last resort is not set",
            "",
            "      10.0.0.0/32 is subnetted, 1 subnets",
            "C        10.1.1.1 is directly connected, Loopback0",
            "      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks",
            "C        192.168.100.0/24 is directly connected, Ethernet0/0",
            "L        192.168.100.1/32 is directly connected, Ethernet0/0",
            "      192.168.200.0/24 is variably subnetted, 2 subnets, 2 masks",
            "C        192.168.200.0/24 is directly connected, Ethernet0/1",
            "L        192.168.200.1/32 is directly connected, Ethernet0/1"
        ]
    ]
}
ok: [192.168.100.2] => {
    "show_result.stdout_lines": [
        [
            "Interface                  IP-Address      OK? Method Status                Protocol",
            "Ethernet0/0                192.168.100.2   YES manual up                    up      ",
            "Ethernet0/1                unassigned      YES unset  administratively down down    ",
            "Ethernet0/2                unassigned      YES unset  administratively down down    ",
            "Ethernet0/3                unassigned      YES unset  administratively down down    ",
            "Loopback0                  10.1.1.1        YES manual up                    up      "
        ],
        [
            "Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP",
            "       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area ",
            "       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2",
            "       E1 - OSPF external type 1, E2 - OSPF external type 2",
            "       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2",
            "       ia - IS-IS inter area, * - candidate default, U - per-user static route",
            "       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP",
            "       + - replicated route, % - next hop override",
            "",
            "Gateway of last resort is not set",
            "",
            "      10.0.0.0/32 is subnetted, 1 subnets",
            "C        10.1.1.1 is directly connected, Loopback0",
            "      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks",
            "C        192.168.100.0/24 is directly connected, Ethernet0/0",
            "L        192.168.100.2/32 is directly connected, Ethernet0/0",
            "D     192.168.200.0/24 [90/307200] via 192.168.100.1, 1w6d, Ethernet0/0"
        ]
    ]
}
ok: [192.168.100.3] => {
    "show_result.stdout_lines": [
        [
            "Interface                  IP-Address      OK? Method Status                Protocol",
            "Ethernet0/0                192.168.100.3   YES manual up                    up      ",
            "Ethernet0/1                unassigned      YES unset  administratively down down    ",
            "Ethernet0/2                unassigned      YES unset  administratively down down    ",
            "Ethernet0/3                unassigned      YES unset  administratively down down    ",
            "Loopback0                  10.1.1.1        YES manual up                    up      "
        ],
        [
            "Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP",
            "       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area ",
            "       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2",
            "       E1 - OSPF external type 1, E2 - OSPF external type 2",
            "       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2",
            "       ia - IS-IS inter area, * - candidate default, U - per-user static route",
            "       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP",
            "       + - replicated route, % - next hop override",
            "",
            "Gateway of last resort is not set",
            "",
            "      10.0.0.0/32 is subnetted, 1 subnets",
            "C        10.1.1.1 is directly connected, Loopback0",
            "      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks",
            "C        192.168.100.0/24 is directly connected, Ethernet0/0",
            "L        192.168.100.3/32 is directly connected, Ethernet0/0",
            "D     192.168.200.0/24 [90/307200] via 192.168.100.1, 1w6d, Ethernet0/0"
        ]
    ]
}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=2    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=2    changed=0    unreachable=0    failed=0

``

Обе команды выполнились на всех устройствах.

Если мы сохраняем результат выполнения команд, как в этом playbook, то вывод будет находится в переменных stdout и stdout_lines в отдельных списках.
То есть, в этих переменных теперь будет находится список, внутри которого находятся списки с выводом команд, по порядку описания их в задаче.

Например, мы могли бы вывести вывод только первой команды, указав:
```
    - name: Debug registered var
      debug: var=show_result.stdout_lines[0]
```

### Обработка ошибок

В модуле встроено распознание ошибок.
Поэтому, если команда выполнена с ошибкой, модуль отобразит, что возникла ошибка.

Например, если сделать ошибку в команде, и запустить playbook еще раз
```
$ ansible-playbook 4_ios_command.yml
SSH password:

PLAY [Run show commands on routers] ********************************************

TASK [run sh ip int br] ********************************************************
fatal: [192.168.100.1]: FAILED! => {"changed": false, "failed": true, "msg":
 "matched error in response: shw ip int br\r\n     ^\r\n% Invalid input detected at '^' marker.\r\n\r\nR1#"}
fatal: [192.168.100.2]: FAILED! => {"changed": false, "failed": true, "msg":
 "matched error in response: shw ip int br\r\n     ^\r\n% Invalid input detected at '^' marker.\r\n\r\nR2#"}
fatal: [192.168.100.3]: FAILED! => {"changed": false, "failed": true, "msg":
 "matched error in response: shw ip int br\r\n     ^\r\n% Invalid input detected at '^' marker.\r\n\r\nR3#"}
    to retry, use: --limit @/home/nata/pyneng_course/chapter15/2c_ios_command_fail.retry

PLAY RECAP *********************************************************************
192.168.100.1              : ok=0    changed=0    unreachable=0    failed=1
192.168.100.2              : ok=0    changed=0    unreachable=0    failed=1
192.168.100.3              : ok=0    changed=0    unreachable=0    failed=1
```

То есть, если задача отработала, значит ошибок при выполнении не было.

Аналогичным образом модуль обнаруживает ошибки:
* Ambiguous command
* Incomplete command


