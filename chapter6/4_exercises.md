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


### Задание 6.2
Создать функцию, которая генерирует конфигурацию для trunk-портов.

Аргумент trunk - это словарь trunk-портов. 

Словарь trunk имеет такой формат (тестовый словарь trunk_dict уже создан):
```python
{ 'FastEthernet0/1':['10','20'],
  'FastEthernet0/2':['11','30'],
  'FastEthernet0/4':['17'] }
```

Функция должна возвращать список команд с конфигурацией на основе указанных портов и шаблона trunk_template.

В конце строк в списке не должно быть символа перевода строки.

Проверить работу функции на примере словаря trunk_dict.

```python
def generate_trunk_config(trunk):
    """
    trunk - словарь trunk-портов для которых необходимо сгенерировать конфигурацию.
    
    Возвращает список всех команд, которые были сгенерированы на основе шаблона
    """
    trunk_template = ['switchport trunk encapsulation dot1q',
                      'switchport mode trunk',
                      'switchport trunk native vlan 999',
                      'switchport trunk allowed vlan']

trunk_dict = { 'FastEthernet0/1':['10','20','30'],
               'FastEthernet0/2':['11','30'],
               'FastEthernet0/4':['17'] }
```

### Задание 6.2a
Сделать копию скрипта задания 6.2

Изменить скрипт таким образом, чтобы функция возвращала не список команд, а словарь:
* ключи: имена интерфейсов, вида 'FastEthernet0/1'
* значения: список команд, который надо выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_dict.
```python
def generate_trunk_config(trunk):
    """
    trunk - словарь trunk-портов,
    для которых необходимо сгенерировать конфигурацию, вида:
        { 'FastEthernet0/1':['10','20'], 'FastEthernet0/2':['11','30'], 'FastEthernet0/4':['17'] }
    
    Возвращает словарь:
    - ключи: имена интерфейсов, вида 'FastEthernet0/1'
    - значения: список команд, который надо выполнить на этом интерфейсе
    """
    trunk_template = ['switchport trunk encapsulation dot1q',
                      'switchport mode trunk',
                      'switchport trunk native vlan 999',
                      'switchport trunk allowed vlan']

trunk_dict = { 'FastEthernet0/1':['10','20','30'],
               'FastEthernet0/2':['11','30'],
               'FastEthernet0/4':['17'] }
```

### Задание 6.3
Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает два объекта:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
 * Пример словаря:

```python
{'FastEthernet0/12':'10',
 'FastEthernet0/14':'11',
 'FastEthernet0/16':'17'}
 ```

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
 * Пример словаря:

```python
 {'FastEthernet0/1':['10','20'],
  'FastEthernet0/2':['11','30'],
  'FastEthernet0/4':['17']}
```
Функция ожидает в качестве аргумента имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

### Задание 6.3a
Сделать копию скрипта задания 6.3.

Дополнить скрипт:
* добавить поддержку конфигурации, когда настройка access-порта выглядит так:

```
interface FastEthernet0/20
  switchport mode access
  duplex auto
```
То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
```python
{'FastEthernet0/12':'10',
 'FastEthernet0/14':'11',
 'FastEthernet0/20':'1' }
```
Функция ожидает в качестве аргумента имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

