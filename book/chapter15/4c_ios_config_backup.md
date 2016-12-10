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

