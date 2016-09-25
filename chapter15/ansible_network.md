## Особенности работы Ansible с сетевыми устройствами

Тут речь о доступе к устройствам, через CLI обычное подключение по SSH.

Обратите внимание на такие существующие модули (возможно они решат вашу задачу):
- https://github.com/networktocode/ntc-ansible (пока что возможны проблемы при работе с Ansible 2.x)

Новые модули для работы с сетевым оборудованием (пока что их нет в основном релизе Ansible)
- https://github.com/ansible/ansible-modules-core/tree/devel/network/ios

Если эти модули вам не подходят, то ниже варианты как можно подойти к работе с сетевыми устройствами.

### Выполнение команд show
Команды show можно выполнять используя модуль raw

Пример задачи из playbook:
```yml
    - name: run sh ip int br
      raw: sh ip int br | ex unass
```

### Выполнение нескольких команд за раз
Если не использовать существующие модули для работы с сетевым оборудованием, 
то тогда надо писать собственные, для того чтобы передать несколько команд.

Это несложно, так как в Ansible есть все, для того чтобы максимально упростить взаимодействие самописных модулей с существующей идеологией Ansible.

### Создание своих модулей

Документация Ansible:
- http://docs.ansible.com/ansible/developing_modules.html

### Выполнение самописных модулей из playbook

Самый просто вариант сделать так, чтобы Ansible "видел" новый модуль, это добавить его в локальный каталог library.

Есть несколько вариантов вызова своих модулей из playbook.

__Вариант 1__

Вызывать свой модуль, как и существующие. Прямо в задаче.

Для сетевого оборудования нюанс в том, что нам надо выполнять модуль локально.

За локальное выполнение отвечает строка: delegate_to: 127.0.0.1
```yml
    - name: parse the output of "show ip interface brief"
      cisco_ip_intf_parse: output_text="{{ siib_text.stdout }}"
      delegate_to: 127.0.0.1
```

__Вариант 2__

Запустить скрипт используя модуль command.

Так как нас интересует запуск команды локально, чтобы просто выполнить скрипт, надо не забыть добавить "delegate_to: 127.0.0.1".

```yml
    - name: Send configuration to device
      command: library/generate_config.py {{ ansible_ssh_host }} configs/{{ hostname }}.conf 
      delegate_to: 127.0.0.1
```

__Аналог "delegate_to: 127.0.0.1"__

Вместо "delegate_to: 127.0.0.1" можно использовать такую запись:
```yml
    - name: Send configuration to device
      local_action: command library/generate_config.py {{ ansible_ssh_host }} configs/{{ hostname }}.conf 
```
