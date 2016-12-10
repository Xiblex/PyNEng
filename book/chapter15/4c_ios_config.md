# Модуль ios_config

Модуль ios_config - позволяет настраивать устройства под управлением IOS, а также генерировать шаблоны конфигураций или отправлять команды на основании шаблона.

У модуля ios_config много возможностей и параметров, поэтому начнем с самых простых примеров и постепенно будем добавлять параметры и комбинировать их друг с другом.

Параметры модуля (мы разберемся с каждым параметром и его значениями ниже):
* __after__ - какие действия выполнить после команд
* __before__ - какие действия выполнить до команд
* __backup__ - аргумент, который указывает нужно ли делать резервную копию текущей конфигурации устройства перед внесением изменений. Файл будет копироваться в каталог backup, относительно каталога в котором находится playbook
* __config__ - параметр, который позволяет указать базовый файл конфигурации, с которым будут сравниваться изменения. Если он указан, модуль не будет скачивать конфигурацию с устройства.
* __defaults__ - параметр указывает нужно ли собираться всю информацию с устройства, в том числе и значения по умолчанию. Если включить этот параметр, то модуль будет собирать текущую кофигурацию с помощью команды sh run all. По умолчанию этот параметр отключен и конфигурация проверяется командой sh run
* __lines (commands)__ - список команд, которые должны быть настроены. Команды нужно указывать без сокращений и ровно в том виде, в котором они будут в конфигурации.
* __match__ - параметр указывает как именно нужно сравнивать команды
* __parents__ - название секции, в которой нужно применить команды. Если команда находится внутри вложенной секции, нужно указывать весь путь. Если этот параметр не указан, то считается, что команда должны быть в глобальном режиме конфигурации
* __replace__ - параметр указывает как выполнять настройку устройства
* __save__ - сохранять ли текущую конфигурацию в стартовую. По умолчанию конфигурация не сохраняется
* __src__ - параметр указывает путь к файлу, в котором находится конфигурация или шаблон конфигурации. Взаимоисключающий параметр с lines (то есть, можно указывать или lines или src). Заменяет модуль ios_template, который скоро будет удален.

## lines (commands)

Самый простой способ использовать модуль ios_config - отправлять команды глобального конфигурационного режима с параметром lines (для параметра lines есть alias commands, то есть, можно вместо lines писать commands).

Посмотрим на пример playbook 6_ios_config_lines.yml:
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config password encryption
      ios_config:
        lines:
          - service password-encryption
        provider: "{{ cli }}"
```

Мы, по-прежнему используем переменную cli, которую указали в файле group_vars/all.yml, для того, чтобы указать параметры подключения.

Если мы запустим playbook, то получим такой результат:
```
$ ansible-playbook 6_ios_config_lines.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config password encryption] **********************************************
changed: [192.168.100.2]
changed: [192.168.100.3]
changed: [192.168.100.1]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=1    unreachable=0    failed=0
```

Какие команды Ansible выполняет:
* terminal length 0
* enable
* show running-config - чтобы проверить есть ли эта настройка на устройстве. Если команда есть, задача выполняться не будет. Если команды нет, задача выполнится
* если команды, которая указана в задаче нет в конфигурации:
 * configure terminal
 * service password-encryption
 * end

Так как модуль каждый раз проверяет конфигурацию, прежде чем применит команду, модуль идемпотентен.
То есть, если мы ещё раз запустим playbook, а команда уже настроена, изменения не будут выполнены:
```
$ ansible-playbook 6_ios_config_lines.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config password encryption] **********************************************
ok: [192.168.100.1]
ok: [192.168.100.3]
ok: [192.168.100.2]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0

```

> **Caution** Обязательно пишите команды полностью, а не сокращенно. И обращайте внимание, что, для некоторых команд, IOS сам добавляет параметры. Если писать команду не в том виде, в котором она реально видна в конфигурационном файле, модуль не будет идемпотентен. Он будет всё время считать, что команды нет и вносить изменения каждый раз. 

Параметр lines позволяет отправлять и несколько команд (playbook 6_ios_config_mult_lines.yml):
```
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Send config commands
      ios_config:
        lines:
          - service password-encryption
          - no ip http server
          - no ip http secure-server
          - no ip domain lookup
        provider: "{{ cli }}"
```

Результат выполнения:
```
$ ansible-playbook 6_ios_config_mult_lines.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Send config commands] ****************************************************
changed: [192.168.100.1]
changed: [192.168.100.3]
changed: [192.168.100.2]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=1    unreachable=0    failed=0

```

## parents

Если нам нужно применить команды в каком-то подрежиме, а не в глобальном конфигурационно режиме, нужно использовать параметр parents.

Например, нам нужно применить такие команды:
```
line vty 0 4
 login local
 transport input ssh
```

В таком случае, playbook 6a_ios_config_parents_basic.yml будет выглядеть так:
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        provider: "{{ cli }}"

```

Запуск будет выполняться аналогично предыдущим playbook:
```
$ ansible-playbook 6a_ios_config_parents_basic.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
changed: [192.168.100.3]
changed: [192.168.100.2]
changed: [192.168.100.1]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=1    unreachable=0    failed=0
```

Если нам нужно выполнить команду в нескольких вложенных режимах, мы указываем подрежимы в списке parents.
Например, нам нужно выполнить такие команды:

```
policy-map OUT_QOS
 class class-default
  shape average 100000000 1000000
```

Тогда playbook 6a_ios_config_parents_mult.yml будет выглядеть так:
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config QoS policy
      ios_config:
        parents:
          - policy-map OUT_QOS
          - class class-default
        lines:
          - shape average 100000000 1000000
        provider: "{{ cli }}"
```


## Отображение обновлений

Попробуем сделать playbook, который не только отправляет команды, но и показывает какие именно изменения были сделаны.
Сделаем это на примере  playbook 6a_ios_config_parents_basic.yml.
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        provider: "{{ cli }}"

```

Для того, чтобы playbook что-то менял, нужно сначала отменить команды. Либо вручную, либо изменив playbook.
Например, на маршрутизаторе 192.168.100.1 вместо строки transport input ssh, вручную пропишем строку transport input all.

Для начала, попробуем вывести изменения с помощью опции verbose:
```
$ ansible-playbook 6a_ios_config_parents_basic.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
ok: [192.168.100.3] => {"changed": false, "warnings": []}
changed: [192.168.100.1] => {"changed": true, "updates": ["line vty 0 4", "transport input ssh"], "warnings": []}
ok: [192.168.100.2] => {"changed": false, "warnings": []}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0
```

В выводе, в поле updates видно, какие именно команды Ansible отправил на устройство.
Обратите внимание, что команда login local не отправлялась, так как она настроена.

Изменения были выполнены только на маршрутизаторе 192.168.100.1.
Ещё один важный момент - поле updates в выводе есть только в том случае, когда есть изменения.

И, хотя мы можем пользоваться таким вариантом, чтобы отобразить изменения, было бы удобней, чтобы информация отображалась только для тех устройств, для которых произошли изменения.
А в случае с режимом verbose, мы видим информацию обо всех устройствах.

Сделаем новый playbook 6b_ios_config_debug.yml на основе 6a_ios_config_parents_basic.yml таким образом:
```
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        provider: "{{ cli }}"
      register: cfg

    - name: Show config updates
      debug: var=cfg.updates
      when: cfg.changed == true

```
Изменения в playbook:
* Теперь мы сохраняем результат работы первой задачи в переменную __cfg__.
* Затем в отдельной задаче используем модуль __debug__ для того, чтобы показать содержимое поля __updates__.
 * так как поле updates в выводе есть только в том случае, когда есть изменения, мы ставим условие when, которое проверяет были ли изменения.
 * задача будет выполняться только тогда, когда на устройстве были внесены изменения.
 * when: cfg.changed эквивалентно записи when: cfg.changed == true

Если запустить повторно playbook, когда изменений не было, задача Show config updates, пропускается:
```
$ ansible-playbook 6b_ios_config_debug.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
ok: [192.168.100.2]
ok: [192.168.100.3]
ok: [192.168.100.1]

TASK [Show config updates] *****************************************************
skipping: [192.168.100.1]
skipping: [192.168.100.2]
skipping: [192.168.100.3]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0
```

Если теперь опять вручную изменить конфигурацию маршрутизатора 192.168.100.1 (изменить transport input ssh на transport input all):
```
$ ansible-playbook 6b_ios_config_debug.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
ok: [192.168.100.2]
changed: [192.168.100.1]
ok: [192.168.100.3]

TASK [Show config updates] *****************************************************
ok: [192.168.100.1] => {
    "cfg.updates": [
        "line vty 0 4",
        "transport input ssh"
    ]
}
skipping: [192.168.100.2]
skipping: [192.168.100.3]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0

```

Теперь второе задание отображает информацию о том, какие именно изменения были внесены на маршрутизаторе.

## save

Параметр __save__ позволяет указать нужно ли сохранять текущую конфигурацию в стартовую. По умолчанию, значение параметра - __no__.

Доступные варианты значений:
* no (или false)
* yes (или true)

К сожалению, на данный момент (версия ansible 2.2), этот параметр не отрабатывает корректно, так как на устройство отправляется команда copy running-config startup-config, но, при этом, не отправляется подтверждение на сохранение.
Из-за этого, при запуске playbook с параметром save выставленным в yes, появляется такая ошибка:
```
$ ansible-playbook 6с_ios_config_save.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
fatal: [192.168.100.3]: FAILED! => {"changed": false, "failed": true, "msg":
 "timeout trying to send command: copy running-config startup-config\r"}
fatal: [192.168.100.1]: FAILED! => {"changed": false, "failed": true, "msg":
 "timeout trying to send command: copy running-config startup-config\r"}
fatal: [192.168.100.2]: FAILED! => {"changed": false, "failed": true, "msg":
 "timeout trying to send command: copy running-config startup-config\r"}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=0    changed=0    unreachable=0    failed=1
192.168.100.2              : ok=0    changed=0    unreachable=0    failed=1
192.168.100.3              : ok=0    changed=0    unreachable=0    failed=1

```

Но, мы можем самостоятельно сделать сохранение, используя модуль ios_command (а позже мы посмотрим как сделать это же, с помощью параметра after).

На основе playbook 6a_ios_config_parents_basic.yml сделаем playbook с сохранением конфигурации 6c_ios_config_save.yml:
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        #save: yes - в версии 2.2 не работает корректно
        provider: "{{ cli }}"
      register: cfg

    - name: Save config
      ios_command:
        commands:
          - write
        provider: "{{ cli }}"
      when: cfg.changed
```

Если мы снова изменим в конфигурации маршрутизатора 192.168.100.1 строку transport input all на transport input ssh, запуск playbook будет выглядеть так:
```
$ ansible-playbook 6c_ios_config_save.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
ok: [192.168.100.3]
ok: [192.168.100.2]
changed: [192.168.100.1]

TASK [Save config] *************************************************************
skipping: [192.168.100.2]
skipping: [192.168.100.3]
ok: [192.168.100.1]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0

```

## backup

Параметр __backup__ указывает нужно ли делать резервную копию текущей конфигурации устройства перед внесением изменений.
Файл будет копироваться в каталог backup, относительно каталога в котором находится playbook (если каталог не существует, он будет создан).

Playbook 6d_ios_config_backup.yml:
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        backup: yes
        provider: "{{ cli }}"
```

Теперь, каждый раз, когда мы запускаем playbook (даже если не нужно вносить изменения в конфигурацию), в каталог backup будет копироваться текущая конфигурация:
```
$ ansible-playbook 6d_ios_config_backup.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
ok: [192.168.100.1] => {"backup_path":
 "/home/nata/pyneng_course/chapter15/backup/192.168.100.1_config.2016-12-10@12:35:38",
 "changed": false, "warnings": []}
ok: [192.168.100.3] => {"backup_path":
 "/home/nata/pyneng_course/chapter15/backup/192.168.100.3_config.2016-12-10@12:35:38",
 "changed": false, "warnings": []}
ok: [192.168.100.2] => {"backup_path":
 "/home/nata/pyneng_course/chapter15/backup/192.168.100.2_config.2016-12-10@12:35:38",
 "changed": false, "warnings": []}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0
```

В каталоге backup файлы такого вида (при каждом запуске playbook они перезаписываются):
```
192.168.100.1_config.2016-12-10@10:42:34
192.168.100.2_config.2016-12-10@10:42:34
192.168.100.3_config.2016-12-10@10:42:34
```

## defaults

Параметр __defaults__ указывает нужно ли собираться всю информацию с устройства, в том числе и значения по умолчанию.
Если включить этот параметр, то модуль будет собирать текущую кофигурацию с помощью команды sh run all.
По умолчанию этот параметр отключен и конфигурация проверяется командой sh run.

Этот параметр полезен в том случае, если мы указываем в настройках команду, которая не видна в конфигурации.
Например, такое может быть, когда мы указали параметр, который и так используется по умолчанию.

Если мы не будем использовать параметр defaults, и укажем команду со значением, по умолчанию (например, в playbook ниже мы указываем команду ip mtu 1500), то каждый раз, когда мы запускаем playbook, будут вноситься изменения.
Присходит это потому, что Ansible каждый раз вначале проверяет наличие команд в соответствующем режиме.
Если команд нет, то соответствующая задача выполняется.


В такой варианте playbook 6e_ios_config_defaults.yml каждый раз будут вноситься изменения (попробуйте самостоятельно):
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config interface
      ios_config:
        parents:
          - interface Ethernet0/2
        lines:
          - ip address 192.168.200.1 255.255.255.0
          - ip mtu 1500
        provider: "{{ cli }}"
```

Если же мы добавим параметр defaults: yes, изменения уже не будут внесены, если не хватало только команды ip mtu 1500 (playbook 6e_ios_config_defaults.yml):
```
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config interface
      ios_config:
        parents:
          - interface Ethernet0/2
        lines:
          - ip address 192.168.200.1 255.255.255.0
          - ip mtu 1500
        defaults: yes
        provider: "{{ cli }}"
```

Запуск playbook:
```
$ ansible-playbook 6e_ios_config_defaults.yml
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config interface] ********************************************************
ok: [192.168.100.1]
ok: [192.168.100.3]
ok: [192.168.100.2]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0

```

## after

Параметр __after__ указывает какие команды выполнить после команд в списке lines (или commands).

Команды, которые указаны в параметре after:
* выполняются только если должны быть внесены изменения.
* при этом они будут выполнены, независимо от того есть они в конфигурации или нет.

Параметр after очень полезен в ситуациях, когда нам нужно выполнить команду, которая не сохраняется в конфигурации.
Например, команда no shutdown не сохраняется в конфигурации маршрутизатора.
И, если бы мы написали её в списке lines, то изменения вносились бы каждый раз, при выполнении playbook. 

Но, если мы напишем команду no shutdown в списке after, то только в том случае, если нужно вносить изменения (согласно списка lines), будет применена и команда no shutdown.

Пример использования параметра after в playbook 6f_ios_config_after.yml:
```yml
---

- name: Run cfg commands on router
  hosts: 192.168.100.1
  gather_facts: false
  connection: local

  tasks:

    - name: Config interface
      ios_config:
        parents:
          - interface Ethernet0/3
        lines:
          - ip address 192.168.230.1 255.255.255.0
        after:
          - no shutdown
        provider: "{{ cli }}"
```

Первый запуск playbook, с внесением изменений:
```
$ ansible-playbook 6f_ios_config_after.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
SSH password:

PLAY [Run cfg commands on router] *********************************************

TASK [Config interface] ********************************************************
changed: [192.168.100.1] => {"changed": true, "updates": ["interface Ethernet0/3",
 "ip address 192.168.230.1 255.255.255.0", "no shutdown"], "warnings": []}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
```

Второй запуск playbook (изменений нет, поэтому команда no shutdown не выполняется):
```
$ ansible-playbook 6f_ios_config_after.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config interface] ********************************************************
ok: [192.168.100.1] => {"changed": false, "warnings": []}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=0    unreachable=0    failed=0

```

Рассмотрим ещё один пример использования after.
Сохраним, с помощью after, конфигурацию устройства (playbook 6f_ios_config_after_save.yml):
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        after:
          - end
          - write
        provider: "{{ cli }}"
```

Результат выполнения playbook (изменения только на маршрутизаторе 192.168.100.1):
```
$ ansible-playbook 6f_ios_config_after_save.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
SSH password:

PLAY [Run cfg commands on routers] *********************************************

TASK [Config line vty] *********************************************************
ok: [192.168.100.2] => {"changed": false, "warnings": []}
ok: [192.168.100.3] => {"changed": false, "warnings": []}
changed: [192.168.100.1] => {"changed": true, "updates": ["line vty 0 4",
 "transport input ssh", "end", "write"], "warnings": []}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0

```


## before

Параметр __before__ указывает какие действия выполнить до команд в списке lines.

Команды, которые указаны в параметре before:
* выполняются только если должны быть внесены изменения.
* при этом они будут выполнены, независимо от того есть они в конфигурации или нет.

Параметр before полезен в ситуациях, когда вам нужно выполнить какуе-то действия перед выполнением команд в списке lines.
При этом, также как и параметр after, параметр before не влияет на то, какие команды сравниваются с конфигурацией.
То есть, по-прежнему, сравниваются только команды в списке lines.

Playbook 6g_ios_config_before.yml:
```yml
---

- name: Run cfg commands on router
  hosts: 192.168.100.1
  gather_facts: false
  connection: local

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
        provider: "{{ cli }}"
```

В playbook 6g_ios_config_before.yml мы сначала удаляем ACL IN_to_OUT с помощью параметра before, а затем создаем его заново.
Таким образом мы будем уверены всегда, что в этом ACL находятся только те строки, которые мы задали в списке lines.

Запуск playbook с изменениями:
```
$ ansible-playbook 6g_ios_config_before.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
SSH password:

PLAY [Run cfg commands on router] **********************************************

TASK [Config ACL] **************************************************************
changed: [192.168.100.1] => {"changed": true, "updates":
 ["no ip access-list extended IN_to_OUT", "ip access-list extended IN_to_OUT",
 "permit tcp 10.0.1.0 0.0.0.255 any eq www",
 "permit tcp 10.0.1.0 0.0.0.255 any eq 22",
 "permit icmp any any"], "warnings": []}

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=1    unreachable=0    failed=0
```

Запуск playbook без изменений (команда в списке before не выполняется):
```


## match

## replace


## src
