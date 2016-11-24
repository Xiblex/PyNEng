# Playbooks

Playbook (файл сценариев) — это файл в котором описываются действия, которые нужно выполнить на какой-то группе хостов.

Внутри playbook:
* play - это набор задач, которые нужно выполнить для группы хостов
* task - это конкретная задача. В задаче есть, как минимум:
 * описание
 * модуль и команда (действие в модуле)


Посмотрим на простой пример plabook (файл 1_show_commands_with_raw.yml):
```yaml
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
<script src="https://gist.github.com/natenka/feb3768494561ae5c93a230d77cd6958.js"></script>

{% gist id="natenka/feb3768494561ae5c93a230d77cd6958" %}{% endgist %}

В этом playbook у нас два сценария (play). Разберемся с первым:
* 'Run show commands on routers' - будет применяться к устройствам в группе cisco-routers
 * ```gather_facts: false``` - в данном случае, нам нужно отключить сбор фактов (информации) об устройстве, так как для сетевого оборудования надо использовать отдельные модули для сбора фактов.
   * в разделе [конфигурационный файл](book/chapter15/2_configuration.md) мы рассматривали как отключить сбор фактов по умолчанию. Если вы его отключили в конфигурационном файле, то параметр gather_facts в play не нужно указывать.
 * дальше идет перечень задач
   * в каждой задаче должно быть имя и действие. Действие может быть только одно.
   * в действии мы указываем какой модуль использовать и параметры модуля.

И тот же playbook с отображением элементов:

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/book/chapter15/images/playbook.png)

<details> 
  <summary>Вывод запуска playbook (в цвете)</summary>
<img src=https://raw.githubusercontent.com/natenka/PyNEng/master/book/chapter15/images/playbook_execution.png alt="Ansible Playbook">
</details>
