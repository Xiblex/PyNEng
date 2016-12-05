## Модуль ios_command

Модуль ios_command - отправляет команду на устройство под управлением IOS и возвращает результат выполнения команды.

Обратите внимание, что этот модуль не поддерживает отправку команду в конфигурационном режиме.
Для этого используется отдельный модуль - ios_config.



```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100
```

```
[defaults]

inventory = ./myhosts

remote_user = cisco
ask_pass = True
```

group_vars/all.yml
```
---

cli:
  host: "{{ inventory_hostname }}"
  username: "cisco"
  password: "cisco"
  transport: cli
  authorize: yes
  auth_pass: "cisco"
```
