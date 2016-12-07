## Работа с результатами выполнения модуля

До сих пор мы только отправляли команды на устройства и никак не работали с результатом.
Как минимум, нам нужно знать как посмотреть на вывод команды.

В этом разделе мы посмотрим на то, как можно получать результаты выполнения команды, отображать их, использовать в следующих действиях.

Примеры будут использовать модуль raw.
Но аналогичные принципы будут работать и с другими модулями.

### verbose

Мы уже видели один из способов показать результат выполнения модуля - флаг verbose.

Конечно, вывод не особо удобно читать, но, как минимум, мы видим, что команды выполнились.
Также этот флаг позволяет подробно посмотреть какие шаги выполняет Ansible.

Пример запуска playbook с флагом verbose (вывод сокращен):
```
ansible-playbook 1_show_commands_with_raw.yml -v
...
TASK [run sh vlan] *************************************************************
changed: [192.168.100.100] => {"changed": true, "rc": 0, "stderr": "Shared connection to 192.168.100.100 closed.\r\n", "stdout": "\r\n\r\nVLAN Name                             Status    Ports\r\n---- -------------------------------- --------- -------------------------------\r\n1    default                          active    Et0/0, Et0/1, Et0/2, Et0/3\r\n                                                Et1/1, Et1/2, Et1/3, Et2/0\r\n                                                Et2/1, Et2/2, Et2/3, Et3/0\r\n                                                Et3/1, Et3/2, Et3/3\r\n2    VLAN0002                         active    \r\n1002 fddi-default                     act/unsup \r\n1003 token-ring-default               act/unsup \r\n1004 fddinet-default                  act/unsup \r\n1005 trnet-default                    act/unsup \r\n\r\nVLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2\r\n---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------\r\n1    enet  100001     1500  -      -      -        -    -        0      0   \r\n2    enet  100002     1500  -      -      -        -    -        0      0   \r\n1002 fddi  101002     1500  -      -      -        -    -        0      0   \r\n1003 tr    101003     1500  -      -      -        -    -        0      0   \r\n1004 fdnet 101004     1500  -      -      -        ieee -        0      0   \r\n1005 trnet 101005     1500  -      -      -        ibm  -        0      0   \r\n\r\nPrimary Secondary Type              Ports\r\n------- --------- ----------------- ------------------------------------------\r\n", "stdout_lines": ["", "", "VLAN Name                             Status    Ports", "---- -------------------------------- --------- -------------------------------", "1    default                          active    Et0/0, Et0/1, Et0/2, Et0/3", "                                                Et1/1, Et1/2, Et1/3, Et2/0", "                                                Et2/1, Et2/2, Et2/3, Et3/0", "                                                Et3/1, Et3/2, Et3/3", "2    VLAN0002                         active    ", "1002 fddi-default                     act/unsup ", "1003 token-ring-default               act/unsup ", "1004 fddinet-default                  act/unsup ", "1005 trnet-default                    act/unsup ", "", "VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2", "---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------", "1    enet  100001     1500  -      -      -        -    -        0      0   ", "2    enet  100002     1500  -      -      -        -    -        0      0   ", "1002 fddi  101002     1500  -      -      -        -    -        0      0   ", "1003 tr    101003     1500  -      -      -        -    -        0      0   ", "1004 fdnet 101004     1500  -      -      -        ieee -        0      0   ", "1005 trnet 101005     1500  -      -      -        ibm  -        0      0   ", "", "Primary Secondary Type              Ports", "------- --------- ----------------- ------------------------------------------"]}
```

При увеличении количества букв v в флаге, вывод становится более подробным.
Попробуйте вызывать этот же playbook и добавлять к флагу буквы v (5 и больше показывают одинаковый вывод).

Несмотря на то, что вывод не очень приятен для восприятия, мы видим, что в результаты выполнения задачи, мы получаем объект в формате JSON, с такими полями:
* changed - ключ, который указывает были ли внесены изменения
* rc - return code. Это поле будет появляться в выводе тех модулей, которые выполняют какие-то команды
* stderr - ошибки, при выполнении команды. Это поле будет появляться в выводе тех модулей, которые выполняют какие-то команды
* stdout - вывод команды
* stdout_lines - вывод команды разбитый построчно


### register

Параметр __register__ позволяет сохранить результат выполнения модуля в переменную.
Затем эта переменная может использоваться в шаблонах, в принятии решений о ходе сценария и отображении вывода.

Попробуем сохранить результат выполнения команды.
Для этого будем использовать такой playbook:
```
---

- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: sh ip int br | ex unass
      register: sh_ip_int_br_result
```

Если запустить этот playbook, вывод не будет отличаться, так как мы отлько записали вывод в переменную, но ничего с ней не делаем.
Попробуем отобразить результат выполнения команды - для этого будем использовать модуль debug.


### debug

Модуль debug позволяет отображать информацию на стандартный поток вывода.
Это может произвольная строка, переменная, которую мы сохранили ранее или какие-то переменные, которые определили мы или те, которые получены в результате сбора фактов об устройстве.


Для отображения сохраненный результатов выполнения команды, добавим задание в playbook:
```
---

- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: sh ip int br | ex unass
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug: var=sh_ip_int_br_result.stdout_lines
```

Обратите внимание, что мы выводим не всё содержимое переменной sh_ip_int_br_result, а только содержимое stdout_lines.
Таким образом вы увидим структурированный вывод.

Результат запуска playbook будет выглядеть  так:
```
$ ansible-playbook 2_register_vars.yml
SSH password:

PLAY [Run show commands on routers] ********************************************

TASK [run sh ip int br] ********************************************************
changed: [192.168.100.1]
changed: [192.168.100.2]
changed: [192.168.100.3]

TASK [Debug registered var] ****************************************************
ok: [192.168.100.1] => {
    "sh_ip_int_br_result.stdout_lines": [
        "",
        "Interface                  IP-Address      OK? Method Status                Protocol",
        "Ethernet0/0                192.168.100.1   YES NVRAM  up                    up      ",
        "Ethernet0/1                192.168.200.1   YES NVRAM  up                    up      ",
        "Loopback0                  10.1.1.1        YES manual up                    up      "
    ]
}
ok: [192.168.100.2] => {
    "sh_ip_int_br_result.stdout_lines": [
        "",
        "Interface                  IP-Address      OK? Method Status                Protocol",
        "Ethernet0/0                192.168.100.2   YES manual up                    up      ",
        "Loopback0                  10.1.1.1        YES manual up                    up      "
    ]
}
ok: [192.168.100.3] => {
    "sh_ip_int_br_result.stdout_lines": [
        "",
        "Interface                  IP-Address      OK? Method Status                Protocol",
        "Ethernet0/0                192.168.100.3   YES manual up                    up      ",
        "Loopback0                  10.1.1.1        YES manual up                    up      "
    ]
}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.3              : ok=2    changed=1    unreachable=0    failed=0
```


### register, debug, when

С помощью ключевого слова __when__, можно указать условие, при выполнении которого, задача выполняется.
Если условие не выполняется, то задача пропускается.

Например, создадим такой playbook 3_register_debug_when.yml:
```
---

- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: sh ip int bri | ex unass
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug:
        msg: "Error in command"
      when: "'invalid' in sh_ip_int_br_result.stdout"
```

В последнем задании у нас несколько изменений:
* модуль debug теперь отображает не содержимое сохраненной переменной, а сообщение, которое мы указали в переменной msg.
* условие when позволяет указать, что данное задание будет выполняться только если условие будет выполнено
 * when: "'invalid' in sh_ip_int_br_result.stdout" - это условие означает, что задача будет выполнена только в том случае, если в выводе sh_ip_int_br_result.stdout будет найдена строка invalid (например, когда неправильно введена команда)

Сначала попробуем выполнить playbook:
```
$ ansible-playbook 3_register_debug_when.yml
SSH password:

PLAY [Run show commands on routers] ********************************************

TASK [run sh ip int br] ********************************************************
changed: [192.168.100.1]
changed: [192.168.100.2]
changed: [192.168.100.3]

TASK [Debug registered var] ****************************************************
skipping: [192.168.100.1]
skipping: [192.168.100.2]
skipping: [192.168.100.3]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=1    unreachable=0    failed=0

```

Обратите внимание на сообщения skipping - это означает, что задача не выполнялась для указанных устройств.
Не выполнилась она потому, что условие в when не было выполнено.

Теперь попробуем тот же playbook, но сделаем ошибку в команде:
```
---

- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: shh ip int bri | ex unass
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug:
        msg: "Error in command"
      when: "'invalid' in sh_ip_int_br_result.stdout"
```

Теперь результат выполнения будет таким:
```
$ ansible-playbook 3_register_debug_when.yml
SSH password:

PLAY [Run show commands on routers] ********************************************

TASK [run sh ip int br] ********************************************************
changed: [192.168.100.1]
changed: [192.168.100.2]
changed: [192.168.100.3]

TASK [Debug registered var] ****************************************************
ok: [192.168.100.1] => {
    "msg": "Error in command"
}
ok: [192.168.100.2] => {
    "msg": "Error in command"
}
ok: [192.168.100.3] => {
    "msg": "Error in command"
}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.3              : ok=2    changed=1    unreachable=0    failed=0

```

Теперь мы видим сообщение, которое было указано в задаче для модуля debug, так как команда была с ошибкой.

С помощью условий в when, можно не только генерировать какие-то сообщения с модулем debug, но и контролировать то, какие действия будут выполняться, в зависимости от условия.
