## Поддерживаемые типы устройств

Netmiko поддерживает несколько типов устройств. Актуальный список можно посмотреть в [репозитории](https://github.com/ktbyers/netmiko) модуля.

## Словарь, определяющий параметры устройств
В словаре могут указываться такие параметры:
```python
cisco_router = {'device_type': 'cisco_ios', # предопределенный тип устройства
                'ip': '192.168.1.1', # адрес устройства
                'username': 'user', # имя пользователя
                'password': 'userpass', # пароль пользователя
                'secret': 'enablepass', # пароль режима enable (опциональный)
                'port': 20022, # порт SSH, по умолчанию 22
                 }
```

## Подключиться по SSH

```python
ssh = ConnectHandler(**cisco_router)
```

## Режим enable

Перейти в режим enable:
```python
ssh.enable()
```

Выйти из режима enable:
```python
ssh.exit_enable_mode()
```

## Отправка команд

В netmiko есть несколько способов отправки команд:
* send_command - отправить одну команду
* send_config_set - отправить список команд
* send_config_from_file - отправить команды из файла (использует внутри метод send_config_set)
* send_command_timing - отправить команду и подождать вывод на основании таймера

### ```send_command```

