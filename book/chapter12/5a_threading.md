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

Для начала рассмотрим пример использования модуля threading вместе с последним примером с netmiko.

Так как для работы с threading, удобнее использовать функции, то мы изменим код:
* переведем код подключения по SSH в функцию
* параметры устройств перенесем в отдельный файл в формате YAML

Итоговый код такой (файл выполняет те же действия, что финальная версия в разделе netmiko):
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

Файл с параметрами подключения к устройствам:
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

Замерим время выполнения скрипта с помощью утилиты time (вывод самого скрипта не показан), а затем сравним какое время выполнения будет с использованием модуля threading:
```
nata: $ time cisco netmiko_function.py "sh ip int br"
...
real    0m6.189s
user    0m0.336s
sys     0m0.080s
```

Теперь посмотрим как будет выглядеть код с использованием модуля threading:
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

Прежде чем мы разберемся с кодом, посмотрим на время выполнения кода:
```
nata: $ time cisco netmiko_function_threading.py "sh ip int br"
...
real    0m2.229s
user    0m0.408s
sys     0m0.068s
```

Как видите, время почти в три раза меньше.
Но, надо учесть, что такая ситуация не будет повторяться при большом количестве подключений.

Разберемся с кодом функции conn_threads:
* threading.Thread - класс, который создает поток
 * для инициации потока, мы передаем вызываемый объект - функцию и её аргументы
* th.start() - стартует поток
* threads.append(th) - добавляет объект потока в список
* th.join() - этот метод ожидает пока поток завершит работу
 * таким образом мы ожидаем пока все потоки завершатся и только потом завершаем основную программу
