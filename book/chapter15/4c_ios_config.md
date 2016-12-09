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

Теперь мы сохраняем результат работы первой задачи в переменную cfg.
Затем в отдельной задаче используем модуль debug для того, чтобы покачать содержимое поля updates.
Но, так как поле updates в выводе есть только в том случае, когда есть изменения, мы ставим условие when, которое проверяет были ли изменения.
И задача будет выполняться только тогда, когда изменения были.

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

## before


```
crypto key generate rsa modulus 1024
ip ssh version 2
```
