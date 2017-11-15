{% raw %}
## defaults

Параметр __defaults__ указывает, нужно ли собирать всю информацию с устройства, в том числе и значения по умолчанию.
Если включить этот параметр, модуль будет собирать текущую конфигурацию с помощью команды sh run all.
По умолчанию этот параметр отключен, и конфигурация проверяется командой sh run.

Этот параметр полезен в том случае, если в настройках указывается команда, которая не видна в конфигурации.
Например, такое может быть, когда указан параметр, который и так используется по умолчанию.


Если не использовать параметр defaults и указать команду, которая настроена по умолчанию, то  при каждом запуске playbook будут вноситься изменения.

Происходит это потому, что Ansible каждый раз вначале проверяет наличие команд в соответствующем режиме.
Если команд нет, то соответствующая задача выполняется.


Например, в таком playbook каждый раз будут вноситься изменения (попробуйте запустить его самостоятельно):
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

Если добавить параметр ```defaults: yes```, изменения уже не будут внесены, если не хватало только команды ip mtu 1500 (playbook 6_ios_config_defaults.yml):
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
$ ansible-playbook 6_ios_config_defaults.yml
```
{% endraw %}

![6e_ios_config_default]({{ book.ansible_img_path }}6e_ios_config_defaults.png)


Если на оборудовании большой конфигурационный файл, может возникнуть такая ошибка:
```
fatal: [192.168.100.3]: FAILED! => {"changed": false, "failed": true, "msg": "unable to retrieve current config", "stderr": "timeout trying to send command: b'show running-config all'", "stderr_lines": ["timeout trying to send command: b'show running-config all'"]}
```

Так происходит из-за того, что Ansible не дождался приглашения.
По умолчанию, Ansible ждет вывода команды 10 секунд и для большого конфигурационного файла этого может быть недостаточно.

Установить большее значение таймаута можно в переменной cli, в файле group_vars/all.yml:
```
cli:
  host: "{{ inventory_hostname }}"
  username: "cisco"
  password: "cisco"
  authorize: yes
  auth_pass: "cisco"
  timeout: 100
```

