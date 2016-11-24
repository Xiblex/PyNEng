# Playbooks

Playbook (файл сценариев) — это файл в котором описываются действия, которые нужно выполнить на какой-то группе хостов.

Внутри playbook:
* play - это набор задач, которые нужно выполнить для группы хостов
* task - это конкретная задача. В задаче есть, как минимум:
 * описание (название задачи можно не писать, но очень рекомендуется)
 * модуль и команда (действие в модуле)


## Синтаксис playbook

Playbook описываются в формате YAML.

Поэтому, если вы забыли синтаксис YAML, его можно повторить в [разделе YAML](book/chapter10/3_yaml.md) или в [документации Ansible](http://docs.ansible.com/ansible/YAMLSyntax.html).


### Пример playbook

Посмотрим на простой пример plabook (файл 1_show_commands_with_raw.yml):
```
---

- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br        
      raw: sh ip int br | ex unass

    - name: run sh ip route
      raw: sh ip route


- name: Run show commands on switches
  hosts: cisco-switches
  gather_facts: false

  tasks:

    - name: run sh int status
      raw: sh int status

    - name: run sh vlans
      raw: show vlans
```


В этом playbook у нас два сценария (play). Разберемся с первым:
* ```name: Run show commands on routers``` - это имя сценария (play). Этот параметр обязательно должен быть в любом сценарии
* ```hosts: cisco-routers``` - сценарий будет применяться к устройствам в группе cisco-routers
 * тут может быть указано и несколько групп, например, таким образом: ```hosts: cisco-routers:cisco-switches```. Подробнее, в [документации](http://docs.ansible.com/ansible/intro_patterns.html)
* обычно в play надо указывать параметр __remote_user__. Но, так как мы указали его в конфигурационном файле Ansible, мы можем пропустить его в play.
* ```gather_facts: false``` - в данном случае, нам нужно отключить сбор фактов (информации) об устройстве, так как для сетевого оборудования надо использовать отдельные модули для сбора фактов.
 * в разделе [конфигурационный файл](book/chapter15/2_configuration.md) мы рассматривали как отключить сбор фактов по умолчанию. Если вы его отключили в конфигурационном файле, то параметр gather_facts в play не нужно указывать.
* ```tasks:``` - дальше идет перечень задач
 * в каждой задаче настроено имя (опционально) и действие. Действие может быть только одно.
 * в действии мы указываем какой модуль использовать и параметры модуля.

И тот же playbook с отображением элементов:

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/book/chapter15/images/playbook.png)

Теперь попробуем запустить playbook:
```
$ ansible-playbook 1_show_commands_with_raw.yml
SSH password:

PLAY [Run show commands on routers] ********************************************

TASK [run sh ip int br] ********************************************************
changed: [192.168.100.1]
changed: [192.168.100.3]
changed: [192.168.100.2]

TASK [run sh ip route] *********************************************************
changed: [192.168.100.2]
changed: [192.168.100.1]
changed: [192.168.100.3]

PLAY [Run show commands on switches] *******************************************

TASK [run sh int status] *******************************************************
changed: [192.168.100.100]

TASK [run sh vlans] ************************************************************
changed: [192.168.100.100]

PLAY RECAP *********************************************************************
192.168.100.1              : ok=2    changed=2    unreachable=0    failed=0
192.168.100.100            : ok=2    changed=2    unreachable=0    failed=0
192.168.100.2              : ok=2    changed=2    unreachable=0    failed=0
192.168.100.3              : ok=2    changed=2    unreachable=0    failed=0
```

<details> 
  <summary>Вывод запуска playbook (в цвете)</summary>
<img src=https://raw.githubusercontent.com/natenka/PyNEng/master/book/chapter15/images/playbook_execution.png alt="Ansible Playbook">
</details>


> **Note** Обратите внимание, что для запуска playbook используется другая команда. Для ad-hoc команды, мы использовали команду ansible. А для playbook - ansible-playbook.


