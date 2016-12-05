# Модули для работы с сетевым оборудованием

В предыдущих разделах мы использовали модуль raw для отправки команд на оборудование.
Он универсален и с его помощью можно отправлять команды на любое устройство.

В этом разделе мы разберемся с сетевыми модулями для работы с IOS, которые поддерживает Ansible.

Список всех сетевых модулей, которые поддерживает Ansible в [документации](http://docs.ansible.com/ansible/list_of_network_modules.html).

Обратите внимание, что Ansible очень активно развивается в сторону поддержки работы с сетевым оборудованием, и в следующей версии Ansible, могут быть дополнительные модули. Поэтому, если на момент чтения курса, уже есть следующая версия курса (версия в курсе 2.2), используйте её и посмотрите в документации, какие новые возможности и модули появились.


Ansible поддерживает подключение к сетевому оборудованию через CLI и через API (если оборудование поддерживает).

Мы будем рассматривать такие core модули, для работы с Cisco IOS устройствами:
* ios_command
* ios_config
* ios_facts

А также модуль ntc-ansible, который не входит в core модули ansible.

## Подключение к сетевому оборудованию из Ansible

Для работы с сетевым оборудованием, нужно указать ряд параметров для подключения к оборудованию.
Все эти параметры должны указываться в аргументе __provider__.

Аргумент __provider__ используется во всех core модулях для работы с сетевым оборудованием и указывает такие параметры:
* host - имя или IP-адрес удаленного устройства
* port - к какому порту подключаться
* username - имя пользователя
* password - пароль
* transport - тип подключения: CLI или API. По умолчанию - cli
* authorize - нужно ли переходить в привилегированный режим (enable, для Cisco)
* auth_pass - пароль для привилегированного режима

Особенность работы с сетевым оборудованием в том, что для каждей задачи нужно указывать параметр provider.
Но, используя переменные, мы можем определить значения в файле переменных, а затем лишь указывать переменную в задаче.

Мы можем указать параметры аргумента provider разными вариантами.

В задаче (task):
```
  tasks:

    - name: run show version
      ios_command:
        commands: show version
        host: "{{ inventory_hostname }}"
        username: cisco
        password: cisco
        transport: cli
```

В переменных playbook:
```
  vars:
    cli:
      host: "{{ inventory_hostname }}"
      username: cisco
      password: cisco
      transport: cli

  tasks:
    - name: run show version
      ios_command:
        commands: show version
        provider: "{{ cli }}"

```

В каталоге group_vars.

Например, в файле group_vars/all.yml:
```
---

cli:
  host: "{{ inventory_hostname }}"
  username: cisco
  password: cisco
  transport: cli
  authorize: yes
  auth_pass: cisco
```

И затем использовать переменную в playbook так же, как и в случае указания переменных в playbook:
```
  tasks:
    - name: run show version
      ios_command:
        commands: show version
        provider: "{{ cli }}"
```

Кроме того, Ansible поддерживает задание параметров в переменных окружения:
* ANSIBLE_NET_USERNAME - для переменной username
* ANSIBLE_NET_PASSWORD - password
* ANSIBLE_NET_SSH_KEYFILE - ssh_keyfile
* ANSIBLE_NET_AUTHORIZE - authorize
* ANSIBLE_NET_AUTH_PASS - auth_pass


Приоритетность значений в порядке возрастания приоритетности:
* значения по умолчанию
* значения переменных окружения
* параметр provider
* аргументы задачи (task)
