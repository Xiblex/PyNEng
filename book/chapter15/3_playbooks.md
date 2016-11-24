# Playbooks

Playbook (файл сценариев) — это файл в котором описываются действия, которые нужно выполнить на какой-то группе хостов.

Внутри playbook:
* play - это набор задач, которые нужно выполнить для группы хостов
* task - это конкретная задача. В задаче есть, как минимум:
 * описание
 * модуль и команда (действие в модуле)


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

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/book/chapter15/images/playbook.png)

<details> 
  <summary>Hidden image</summary>
![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/book/chapter15/images/playbook.png)
</details>
