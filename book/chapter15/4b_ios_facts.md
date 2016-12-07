## Модуль ios_facts

Модуль ios_facts - собирает информацию с устройств под управлением IOS.

Информация берется из таких команд:
* dir
* show version
* show memory statistics
* show interfaces
* show ipv6 interface
* show lldp
* show lldp neighbors detail
* show running-config

В модуле можно указывать какие параметры собирать - можно собирать всю информацию, а можно только подмножество.
По умолчанию, модуль собирает всю информацию, кроме конфигурационного файла.

Какую информацию собирать, указывается в параметре gather_subset.
Поддерживаются такие варианты:
* all
* hardware
* config
* interfaces

Если нужно указать, что нужно собрать все факты:
```
- ios_facts:
    gather_subset: all
    provider: "{{ cli }}"
```

Собрать только подмножество interfaces:
```
- ios_facts:
    gather_subset:
      - interfaces
    provider: "{{ cli }}"
```

Собрать всё, кроме hardware:
```
- ios_facts:
    gather_subset:
      - "!hardware"
    provider: "{{ cli }}"
```

### Использование модуля

Пример playbook 5_ios_facts.yml с использованием модуля ios_facts (собираются все факты):
```
---

- name: Collect IOS facts
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all
        provider: "{{ cli }}"
```


```
$ ansible-playbook 5_ios_facts.yml
SSH password:

PLAY [Collect IOS facts] *******************************************************

TASK [Facts] *******************************************************************
ok: [192.168.100.1]
ok: [192.168.100.2]
ok: [192.168.100.3]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0

```

Для того, чтобы посмотреть, какие именно факты собираются с устройства, можно добавить флаг -v (информация сокращена):
```
$ ansible-playbook 5_ios_facts.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
SSH password:

PLAY [Collect IOS facts] *******************************************************

TASK [Facts] *******************************************************************
ok: [192.168.100.1] => {"ansible_facts": {"ansible_net_all_ipv4_addresses": ["192.168.200.1", "192.168.100.1", "10.1.1.1"], "ansible_net_all_ipv6_addresses": [], "ansible_net_config": }}
...

PLAY RECAP *********************************************************************
192.168.100.1              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.2              : ok=1    changed=0    unreachable=0    failed=0
192.168.100.3              : ok=1    changed=0    unreachable=0    failed=0

```

### Сохранение фактов

В том виде, в котором информация отображается в режиме verbose, довольно сложно понять какая информация собирается об устройствах.
Для того, чтобы лучше понять какая информация собирается об устройствах, в каком формате, скопируем полученную информацию в файл.

Для этого мы будем использовать модуль copy.

Playbook 5a_ios_facts.yml собирает всю информацию об устройствах и записывает в разные файлы:
```
---

- name: Collect IOS facts
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all
        provider: "{{ cli }}"
      register: ios_facts_result

    - name: Copy facts to files
      copy:
        content: "{{ ios_facts_result | to_nice_json }}"
        dest: "all_facts/{{inventory_hostname}}_facts.json"
```




Результат выполнения:
```
$ ansible-playbook 5a_ios_facts.yml
SSH password:

PLAY [Collect IOS facts] *******************************************************

TASK [Facts] *******************************************************************
ok: [192.168.100.1]
ok: [192.168.100.3]
ok: [192.168.100.2]

TASK [Copy facts to files] *****************************************************
changed: [192.168.100.2]
changed: [192.168.100.1]
changed: [192.168.100.3]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.2              : ok=2    changed=1    unreachable=0    failed=0
192.168.100.3              : ok=2    changed=1    unreachable=0    failed=0

```

После этого, в каталоге all_facts находятся такие файлы:
```
192.168.100.1_facts.json
192.168.100.2_facts.json
192.168.100.3_facts.json
```


Сохранение информации об устройствах, не только поможет разобраться, какая информация собирается, но и полезно для дальнейшего использования информации.
