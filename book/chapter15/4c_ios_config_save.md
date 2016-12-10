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

