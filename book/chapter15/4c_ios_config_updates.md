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

