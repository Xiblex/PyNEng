
Структура:
```
├── configs                                   _
│   ├── london_r1.conf                         |
│   ├── london_r2.conf                         |  Каталог для конфигураций (custom)
│   ├── london_r3.conf                         |
│   └── london_r4.conf                        _|
├── group_vars                                _
│   ├── all.yml                                |
│   ├── cisco-devices                          |
│   │   └── all.yml                            |  Каталог с переменными для групп устройств   
│   └── cisco-routers                          |
│       └── all.yml                           _|
├── host_vars                                 _
│   ├── R1                                     |
│   ├── R2                                     |
│   ├── R3                                     |  Каталог с переменными для устройств 
│   ├── R4                                     |
│   └── SW1                                   _|
├── library                                   _
│   ├── cisco_ip_intf_facts_collect.py         |
│   ├── cisco_ip_intf_facts_combine.py         |
│   ├── cisco_ip_intf_parse.py                 |  Каталог с модулями (custom modules)
│   ├── cisco_ip_intf_parse_write.py           |
│   ├── cisco_scenarios_convert.py             |
│   └── generate_config.py                    _|
├── scenarios                                  |  Каталог с описанием сценария для проверки (custom)
│   └── all.txt                               _|
│── templates                                 _
│   ├── cisco_ios_show_ip_int_brief.template   |  Каталог с шаблонами Jinja2 и TextFSM 
│   └── router.j2                             _|
├── 1_cisco-trace-run.yml                      |
├── 2_device_groups_run_commands.yml           |
├── 3_cisco_ip_collect.yml                     |
├── 4_parse_sh_ip_int_br.yml                   |  Ansible Playbooks
├── 5_push_config.yml                          |
├── 6_new_ios_modules.yml                     _|
├── ansible.cfg                               _|  Ansible config file
└── myhosts                                   _|  Inventory file (Hosts file)
```

В этом каталоге находятся 6 PlayBook:
- __1_cisco-trace-run.yml__: демонстрирует выполнение базовых команд а устройствах Cisco:
  - traceroute и sh ip int br | ex unass
    - используется модуль raw
    - результат выполнения команд регистрируется в переменную
    - можно посмотреть как Ansible "видит" результат выполнения команд
      - для этого раскомментируйте строки с заданиями debug
- __2_device_groups_run_commands.yml__: демонстрируется как выполнение задач для разных групп устройств
    - используется модуль raw
- __3_cisco_ip_collect.yml__: показывает как можно работать с самописными модулями
- __4_parse_sh_ip_int_br.yml__: показывает как можно работать с самописными модулями
  - выполняет команду show ip interface brief | exclude unassigned на устройствах
  - регистрирует вывод в переменную
  - передает вывод самописному модулю, который парсит вывод команд с помощью TextFSM
  - получившийся вывод передается следующему модулю, который записывает это а глобальную переменную
- __5_push_config.yml__: использует самописный модуль, чтобы передавать несколько команд на устройство
  - сначала генерируется конфигурация на основане шаблона Jinja
  - затем этот шаблон передается модулю
  - модуль подключается с помощью netmiko к устройствам и передает команды из полученной конфигурации
