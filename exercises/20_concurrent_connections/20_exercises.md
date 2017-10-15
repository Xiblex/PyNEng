# Задания

{% include "../exercises_intro.md" %}


### Задание 20.1

Переделать задание 12.3b таким образом, чтобы проверка доступности устройств
выполнялась не последовательно, а параллельно.

Для этого, необходимо взять за основу функцию check_ip_addresses из задания 11.3.
Функцию надо переделать таким образом, чтобы проверка IP-адресов выполнялась
параллельно в разных потоках.

Функция check_ip_addresses ожидает как аргумент список IP-адресов.
И возвращает два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Если какие-то IP-адреса недоступны, функция send_commands должна
вывести сообщение с информацией о том, какие адреса недоступны.


### Задание 20.1a

Переделать функцию check_ip_addresses из задания 20.1 таким образом,
чтобы она позволяла контролировать количество параллельных проверок IP.

Для этого, необходимо добавить новый параметр limit,
со значением по умолчанию - 2.

Функция check_ip_addresses должна проверять адреса из списка
таким образом, чтобы в любой момент времени максимальное количество
параллельных проверок было равным limit.


### Задание 20.2

В задании используется пример из раздела про [модуль threading](../../book/20_concurrent_connections/5a_threading.md).

Переделать пример таким образом, чтобы:
* вместо функции connect_ssh, использовалась функция send_commands из задания 19.3
 * переделать функцию send_commands, чтобы использовалась очередь и функция conn_threads по-прежнему возвращала словарь с результатами.
 * Проверить работу со списком команд, с командами из файла, с командой show 

Подсказка: threading.Thread может передавать функции не только позиционные аргументы, но и ключевые:
```python
def conn_threads(function, arg1, arg2, **kwargs_dict):

    for some in something:
        th = threading.Thread(target=function,
                              args=(arg1, arg2),
                              kwargs=kwargs_dict)
```

Пример из раздела:
```python
import threading
from queue import Queue
from pprint import pprint
from netmiko import ConnectHandler


COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))


def connect_ssh(device_dict, command, queue):
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print("Connection to device {}".format(device_dict['ip']))

        #Добавляем словарь в очередь
        queue.put({device_dict['ip']: result})


def conn_threads(function, devices, command):
    threads = []
    q = Queue()

    for device in devices:
        # Передаем очередь как аргумент, функции
        th = threading.Thread(target=function, args=(device, command, q))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    results = []
    # Берем результаты из очереди и добавляем их в список results
    for t in threads:
        results.append(q.get())

    return results

pprint(conn_threads(connect_ssh, devices['routers'], COMMAND))

```


### Задание 20.2a

Использовать функции полученные в результате выполнения задания 20.2.

Переделать функцию conn_threads таким образом, чтобы с помощью аргумента limit,
можно было указывать сколько подключений будут выполняться параллельно.
По умолчанию, значение аргумента должно быть 2.

Изменить функцию соответственно, так, чтобы параллельных подключений выполнялось столько,
сколько указано в аргументе limit.

Теперь, если в сумме надо подключиться к 5 устройствам, а параметр limit = 2,
функция выполнит подключения сначала к 1 и 2 устройству параллельно,
затем аналогично к 3 и 4, и затем к 5.


### Задание 20.3

В задании используется пример из раздела про [модуль multiprocessing](book/chapter12/5b_multiprocessing.md).

Переделать пример таким образом, чтобы:
* вместо функции connect_ssh, использовалась функция send_commands из задания 19.3
 * переделать функцию send_commands, чтобы использовалась очередь и функция conn_processes по-прежнему возвращала словарь с результатами.
 * Проверить работу со списком команд, с командами из файла, с командой show

Подсказка: multiprocessing.Process может передавать функции не только позиционные аргументы, но и ключевые:
```python
def conn_processes(function, arg1, arg2, **kwargs_dict):

    for some in something:
        p = multiprocessing.Process(target=function,
                                    args=(arg1, arg2),
                                    kwargs=kwargs_dict)
```

Пример из раздела:
```python
import multiprocessing
import sys
import yaml
from pprint import pprint

from netmiko import ConnectHandler


COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))


def connect_ssh(device_dict, command, queue):
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)

        print("Connection to device {}".format(device_dict['ip']))
        queue.put({device_dict['ip']: result})


def conn_processes(function, devices, command):
    processes = []
    queue = multiprocessing.Queue()

    for device in devices:
        p = multiprocessing.Process(target=function,
                                    args=(device, command, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = []
    for p in processes:
        results.append(queue.get())

    return results

pprint((conn_processes(connect_ssh, devices['routers'], COMMAND)))

```

### Задание 20.3a

Использовать функции полученные в результате выполнения задания 20.3.

Переделать функцию conn_processes таким образом, чтобы с помощью аргумента limit,
можно было указывать сколько подключений будут выполняться параллельно.
По умолчанию, значение аргумента должно быть 2.

Изменить функцию соответственно, так, чтобы параллельных подключений выполнялось столько,
сколько указано в аргументе limit.

Теперь, если в сумме надо подключиться к 5 устройствам, а параметр limit = 2,
функция выполнит подключения сначала к 1 и 2 устройству параллельно,
затем аналогично к 3 и 4, и затем к 5.


