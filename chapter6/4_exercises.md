#Упражнения

### Задание 6.1

Создать функцию, которая генерирует конфигурацию для access-портов.

Аргумент access - это словарь access-портов, вида:
```python
{'FastEthernet0/12':'10',
 'FastEthernet0/14':'11',
 'FastEthernet0/16':'17',
 'FastEthernet0/17':'150'}
```

Функция должна возвращать список всех портов в режиме access
с конфигурацией на основе шаблона access_template.

В конце строк в списке не должно быть символа перевода строки.

Проверить работу функции на примере словаря access_dict.

```python
def generate_access_config(access):
    """
    access - словарь access-портов,
    для которых необходимо сгенерировать конфигурацию, вида:
        { 'FastEthernet0/12':'10','FastEthernet0/14':'11','FastEthernet0/16':'17'}
    
    Возвращает список всех портов в режиме access с конфигурацией на основе шаблона
    """
    access_template = ['switchport mode access',
                       'switchport access vlan',
                       'switchport nonegotiate',
                       'spanning-tree portfast',
                       'spanning-tree bpduguard enable']


access_dict = { 'FastEthernet0/12':'10',
                'FastEthernet0/14':'11',
                'FastEthernet0/16':'17',
                'FastEthernet0/17':'150' }
```

### Задание 6.1a
Сделать копию скрипта задания 6.1.

Дополнить скрипт:
* ввести дополнительный аргумент, который контролирует будет ли настроен port-security
 * имя аргумента 'psecurity'
 * по умолчанию значение False

Проверить работу функции на примере словаря access_dict,
с генерацией конфигурации port-security и без.
```python
def generate_access_config(access):
    """
    access - словарь access-портов,
    для которых необходимо сгенерировать конфигурацию, вида:
        { 'FastEthernet0/12':'10','FastEthernet0/14':'11','FastEthernet0/16':'17' }
    
    psecurity - контролирует нужна ли настройка Port Security. По умолчанию значение False
        - если значение True, то настройка выполняется с добавлением шаблона port_security
        - если значение False, то настройка не выполняется
    
    Возвращает список всех команд, которые были сгенерированы на основе шаблона
    """

    access_template = ['switchport mode access',
                       'switchport access vlan',
                       'switchport nonegotiate',
                       'spanning-tree portfast',
                       'spanning-tree bpduguard enable']

    port_security = ['switchport port-security maximum 2',
                     'switchport port-security violation restrict',
                     'switchport port-security']

access_dict = { 'FastEthernet0/12':'10',
                'FastEthernet0/14':'11',
                'FastEthernet0/16':'17',
                'FastEthernet0/17':'150' }
```


### Задание 6.1b
Сделать копию скрипта задания 1a.

Изменить скрипт таким образом, чтобы функция возвращала не список команд, а словарь:
* ключи: имена интерфейсов, вида 'FastEthernet0/12'
* значения: список команд, который надо выполнить на этом интерфейсе:
```python
      ['switchport mode access',
       'switchport access vlan 10',
       'switchport nonegotiate',
       'spanning-tree portfast',
       'spanning-tree bpduguard enable']
 ```       

Проверить работу функции на примере словаря access_dict,
с генерацией конфигурации port-security и без.
```python
def generate_access_config(access):
    """
    access - словарь access-портов,
    для которых необходимо сгенерировать конфигурацию, вида:
        { 'FastEthernet0/12':'10','FastEthernet0/14':'11','FastEthernet0/16':'17' }
    
    psecurity - контролирует нужна ли настройка Port Security. По умолчанию значение False
        - если значение True, то настройка выполняется с добавлением шаблона port_security
        - если значение False, то настройка не выполняется
    
    Функция возвращает словарь:
    - ключи: имена интерфейсов, вида 'FastEthernet0/1'
    - значения: список команд, который надо выполнить на этом интерфейсе
    """

    access_template = ['switchport mode access',
                       'switchport access vlan',
                       'switchport nonegotiate',
                       'spanning-tree portfast',
                       'spanning-tree bpduguard enable']

    port_security = ['switchport port-security maximum 2',
                     'switchport port-security violation restrict',
                     'switchport port-security']




access_dict = { 'FastEthernet0/12':'10',
                'FastEthernet0/14':'11',
                'FastEthernet0/16':'17',
                'FastEthernet0/17':'150' }
```