## Include

До сих пор, каждый playbook был отдельным файлом.
И, хотя для простых сценариев, такой вариант подходит, когда задач становится больше, может понадобиться выполнять одни и те же действия в разных playbook.
И было бы намного удобней, если бы можно было разбить playbook на блоки, которые можно повторно использовать (как в случае с функциями).

Это можно сделать с помощью выражений include (и с помощью ролей, которые мы будем рассматриваться в следующем разделе).

С помощью выражения include, в playbook можно добавлять:
* задачи
* handlers
* сценарий (play)
* файлы с переменными (используют другое ключевое слово)

### Task include

Task include позволяют подключать в текущий playbook файлы с задачами.

Например, создадим каталог tasks и добавим в него два файла с задачами.

Файл tasks/cisco_vty_cfg.yml:
```yml
---

- name: Config line vty
  ios_config:
    parents:
      - line vty 0 4
    lines:
      - exec-timeout 30 0
      - login local
      - history size 100
      - transport input ssh
    provider: "{{ cli }}"
  notify: save config
```

Файл tasks/cisco_ospf_cfg.yml:
```yml
---

- name: Config ospf
  ios_config:
    src: templates/ospf.j2
    provider: "{{ cli }}"
  notify: save config
```

Шаблон templates/ospf.j2 (переменные, которые используются в шаблоне, находятся в файлах с переменными для каждого устройства, в каталоге host_vars):
```
router ospf 1
 router-id {{ mgmnt_ip }}
 ispf
 auto-cost reference-bandwidth 10000
{% for ip in ospf_ints %}
 network {{ ip }} 0.0.0.0 area 0
{% endfor %}
```

Теперь создадим playbook, который будет использовать созданные файлы с задачами.

Playbook 8_playbook_include_tasks.yml:
```yml
---

- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Disable services
      ios_config:
        lines:
          - no ip http server
          - no ip http secure-server
          - no ip domain lookup
        provider: "{{ cli }}"
      notify: save config

    - include: tasks/cisco_ospf_cfg.yml
    - include: tasks/cisco_vty_cfg.yml

  handlers:

    - name: save config
      ios_command:
        commands:
          - write
        provider: "{{ cli }}"
```

В этом playbook специально создана обычная задача.
А также handler, который мы использовали в предыдущем разделе.
Он вызывается и из задачи, которая находится в playbook, и из задач в подключаемых файлах.

Обратите внимание, что строки include находятся на том же уровне, что и задача.

> В конфигурации R1 внесены изменения, чтобы playbook мог выполнить конфигурацию устройства.

Запуск playbook с изменениями:
```
$ ansible-playbook 8_playbook_include_tasks.yml
```

![8_playbook_include_tasks](https://raw.githubusercontent.com/natenka/PyNEng/master/book/chapter15/images/8_playbook_include_tasks.png)



### Handler include

### Play include

### Vars include


