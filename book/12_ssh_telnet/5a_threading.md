## Модуль threading

Модуль threading может быть полезен для таких задач:
* фоновое выполнение каких-то задач:
 * например, отправка почты во время ожидания ответа от пользователя
* параллельное выполнение задач связанных с вводом/выводом
 * ожидание ввода от пользователя
 * чтение/запись файлов
* задачи, где присутствуют паузы:
 * например, паузы с помощью sleep

Однако, следует учитывать, что в ситуациях, когда требуется повышение производительности, засчет использования нескольких процессоров или ядер, нужно использовать модуль multiprocessing, а не модуль threading.

Рассмотрим пример использования модуля threading вместе с последним примером с netmiko.

Так как для работы с threading, удобнее использовать функции, код изменен:
* код подключения по SSH перенесен в функцию
* параметры устройств перенесены в отдельный файл в формате YAML

Файл netmiko_function.py:
```python
from netmiko import ConnectHandler
import sys
import yaml

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command):

    print "Connection to device %s" % device_dict['ip']

    ssh = ConnectHandler(**device_dict)
    ssh.enable()

    result = ssh.send_command(command)
    print result

for router in devices['routers']:
    connect_ssh(router, COMMAND)
```

Файл devices.yaml с параметрами подключения к устройствам:
```yaml
routers:
- device_type: cisco_ios
  ip: 192.168.100.1
  username: cisco
  password: cisco
  secret: cisco
- device_type: cisco_ios
  ip: 192.168.100.2
  username: cisco
  password: cisco
  secret: cisco
- device_type: cisco_ios
  ip: 192.168.100.3
  username: cisco
  password: cisco
  secret: cisco
```

Время выполнения скрипта (вывод скрипта удален):
```
$ time python netmiko_function.py "sh ip int br"
...
real    0m6.189s
user    0m0.336s
sys     0m0.080s
```

Пример использования модуля threading для подключения по SSH с помощью netmiko (файл netmiko_threading.py):
```python
from netmiko import ConnectHandler
import sys
import yaml
import threading

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)

    print "Connection to device %s" % device_dict['ip']
    print result


def conn_threads(function, devices, command):
    threads = []
    for device in devices:
        th = threading.Thread(target = function, args = (device, command))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

conn_threads(connect_ssh, devices['routers'], COMMAND)
```

Время выполнения кода:
```
$ time python netmiko_function_threading.py "sh ip int br"

...
real    0m2.229s
user    0m0.408s
sys     0m0.068s
```

Время почти в три раза меньше.
Но, надо учесть, что такая ситуация не будет повторяться при большом количестве подключений.

Комментарии к функции conn_threads:
* ```threading.Thread``` - класс, который создает поток
 * ему передается функция, которую надо выполнить, и её аргументы
* ```th.start()``` - запуск потока
* ```threads.append(th)``` - поток добавляется в список
* ```th.join()``` - метод ожидает завершения работы потока
 * метод join выполняется для каждого потока в списке. Таким образом основная программа завершится только когда завершат работу все потоки
 * по умолчанию, ```join``` ждет завершения работы потока бесконечно. Но, можно ограничить время ожидания передав ```join``` время в секундах. В таком случае, ```join``` завершится после указанного количества секунд.


### Получение данных из потоков

В предыдущем примере, данные выводились на стандартный поток вывода.
Для полноценной работы с потоками, необходимо также научиться получать данные из потоков.
Чаще всего, для этого используется очередь.


В Python есть модуль Queue, который позволяет создавать разные типы очередей.

> Очередь это структура данных, которая используется и в работе с сетевым оборудованием. Объект Queue.Queue() - это FIFO очередь.

Очередь передается как аргумент в функцию connect_ssh, которая подключается к устройству по SSH. Результат выполнения команды добавляется в очередь.

Пример использования потоков с получением данных (файл netmiko_threading_data.py):
```python
# -*- coding: utf-8 -*-
from netmiko import ConnectHandler
import sys
import yaml
import threading
from Queue import Queue

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command, queue):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)
    print "Connection to device %s" % device_dict['ip']

    #Добавляем словарь в очередь
    queue.put({ device_dict['ip']: result })


def conn_threads(function, devices, command):
    threads = []
    #Создаем очередь
    q = Queue()

    for device in devices:
        # Передаем очередь как аргумент, функции
        th = threading.Thread(target = function, args = (device, command, q))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    results = []
    # Берем результаты из очереди и добавляем их в список results
    for t in threads:
        results.append(q.get())

    return results

print conn_threads(connect_ssh, devices['routers'], COMMAND)
```

Обратите внимание, что в функции connect_ssh добавился аргумент queue.

Очередь вполне можно воспринимать как список:
* метод ```queue.put()``` равнозначен ```list.append()```
* метод ```queue.get()``` равнозначен ```list.pop(0)```

Для работы с потоками и модулем threading, лучше использовать очередь.
Но, конкретно в данном примере, можно было бы использовать и список.


Пример со списком, скорее всего, будет проще понять. Поэтому ниже аналогичный код, но с использованием обычного списка, вместо очереди (файл netmiko_threading_data_list.py):
```python
# -*- coding: utf-8 -*-
from netmiko import ConnectHandler
import sys
import yaml
import threading

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command, queue):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)
    print "Connection to device %s" % device_dict['ip']

    #Добавляем словарь в список
    queue.append({ device_dict['ip']: result })


def conn_threads(function, devices, command):
    threads = []
    q = []

    for device in devices:
        # Передаем список как аргумент, функции
        th = threading.Thread(target = function, args = (device, command, q))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    # Эта часть нам не нужна, так как, при использовании списка,
    # мы просто можем вернуть его
    #results = []
    #for t in threads:
    #    results.append(q.get())

    return q

print conn_threads(connect_ssh, devices['routers'], COMMAND)
```
