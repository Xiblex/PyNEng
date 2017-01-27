## Модуль argparse

argparse - это модуль для обработки аргументов командной строки.

Примеры того, что позволяет делать модуль:
* создавать аргументы и опции, с которыми может вызываться скрипт
* указывать типы аргументов, значения по умолчанию
* указывать какие действия соответствуют аргументам
* выполнять вызов функции, при указании аргумента
* отображать сообщения с подсказами по использованию скрипта

argparse не единственный модуль для обработки аргументов командной строки.
И даже, не единственный такой модуль в стандартной библиотеке.

Мы будем рассматривать только argparse.
Но, если вы столкнетесь с необходимостью использовать подобные модули,
обязательно посмотрите и на те модули, которые не входят в стандартную библиотеку Python.
Например, на [click](http://click.pocoo.org/5/).

> [Очень хорошая статья](https://realpython.com/blog/python/comparing-python-command-line-parsing-libraries-argparse-docopt-click/), которая сравнивает разные модули обработки аргументов командной строки (рассматриваются argparse, click и docopt).


Посмотрим на пример скрипта, на основе примера в разделе subprocess (файл ping_function.py):
```python
import subprocess
from tempfile import TemporaryFile
import argparse

def ping_ip(ip_address, count=3):
    """
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read()


parser = argparse.ArgumentParser(description='Ping script')

parser.add_argument('-a', action="store", dest="ip")
parser.add_argument('-c', action="store", dest="count", default=2, type=int)

args = parser.parse_args()
print args

rc, message = ping_ip( args.ip, args.count )
print message
```

Разберемся с argparse:
* Сначала необходимо создать парсер:
 * ```parser = argparse.ArgumentParser(description='Ping script')```
* затем, мы начинаем добавлять аргументы:
 * ```parser.add_argument('-a', action="store", dest="ip")```
  * аргумент, который мы передадим после опции ```-a```, сохранится в переменную ```ip```
 * ```parser.add_argument('-c', action="store", dest="count", default=2, type=int)```
  * аргумент, который передается после опции ```-c```, будет сохранен в переменную ```count```, но, прежде, будет конвертирован в число. Если аргумент не было указан, по умолчанию, будет значение 2

Строку ```args = parser.parse_args()``` мы указываем, после того как определили все аргументы.

После её выполнения, в переменной ```args``` содержатся все аргументы, которые мы передали скрипту.
И к ним можно обращаться, использую синтаксис ```args.ip```.


Попробуем вызвать скрипт с разными аргументами.

Такой вывод мы получим, если передать оба аргумента:
```
$ python ping_function.py -a 8.8.8.8 -c 5
Namespace(count=5, ip='8.8.8.8')
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=48.673 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.902 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=48.696 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=48 time=50.040 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=48 time=48.831 ms

--- 8.8.8.8 ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.673/49.228/50.040/0.610 ms
```

> Namespace это объект, который возвращает метод parse_args()

Передаем только IP-адрес:
```
$ python ping_function.py -a 8.8.8.8
Namespace(count=2, ip='8.8.8.8')
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=48.563 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.616 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.563/49.090/49.616/0.526 ms
```

Теперь попробуем вызывать скрипт без аргументов:
```
$ python ping_function.py
Namespace(count=2, ip=None)
Traceback (most recent call last):
  File "ping_function.py", line 31, in <module>
    rc, message = ping_ip( args.ip, args.count )
  File "ping_function.py", line 16, in ping_ip
    stderr=temp)
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 566, in check_output
    process = Popen(stdout=PIPE, *popenargs, **kwargs)
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 710, in __init__
    errread, errwrite)
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 1335, in _execute_child
    raise child_exception
TypeError: execv() arg 2 must contain only strings

```

Мы получили ошибку.
Ошибка, возможно, не совсем понятная, так как, если бы не было argparse, и мы вызвали функцию, не указав IP-адрес, мы бы получили ошибку, что не все аргументы указаны.
Но, из-за argparse, фактически аргумент передается, только он равен ```None```.
Это видно в строке ```Namespace(count=2, ip=None)```.

В таком скрипте, очевидно, IP-адрес необходимо указывать всегда.
В argparse мы можем указать, что аргумент является обязательным.

Добавьте, в строке опции ```-a```, в конце ```required=True```:
```python
parser.add_argument('-a', action="store", dest="ip", required=True)
```

Теперь, если мы вызовем скрипт без аргументов, мы получим такой вывод:
```
$ python ping_function.py
usage: ping_function.py [-h] -a IP [-c COUNT]
ping_function.py: error: argument -a is required
```

Теперь мы видим понятное сообщение, что надо указать обязательным аргумент.
И подсказку usage.

Также, благодаря argparse, нам доступен help:
```
$ python ping_function.py -h
usage: ping_function.py [-h] -a IP [-c COUNT]

Ping script

optional arguments:
  -h, --help  show this help message and exit
  -a IP
  -c COUNT
```

Обратите внимание, что в сообщении, все опции, которые мы указывали, находятся в секции `optional arguments`.
argparse сам определяет, что мы указали опцию, так как она начинается с ```-``` и в имени только одна буква.


Попробуем задать IP-адрес, как позиционный аргумент.
И добавим сообщения, которые описывают аргументы.


Файл ping_function_ver2.py:
```python
import subprocess
from tempfile import TemporaryFile

import argparse


def ping_ip(ip_address, count=3):
    """
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read()


parser = argparse.ArgumentParser(description='Ping script')

parser.add_argument('host', action="store", help="IP or name to ping")
parser.add_argument('-c', action="store", dest="count", default=2, type=int,
                    help="Number of packets")

args = parser.parse_args()
print args

rc, message = ping_ip( args.host, args.count )
print message
```

Изменился способ передачи IP-адреса.
Теперь, вместо указания опции ```-a```, можно просто передать IP-адрес.
Он будет автоматически сохранен в переменной ```host```.
И автоматически считается обязательным.

То есть, нам не нужно указывать ```required=True``` и ```dest="ip"```.


Кроме того, мы указали сообщения, которые будут выводиться, при вызове help.

Теперь вызов скрипта будет выглядеть так:
```
$ python ping_function_ver2.py 8.8.8.8 -c 2
Namespace(host='8.8.8.8', count=2)
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.203 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=51.764 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.203/50.484/51.764/1.280 ms
```

А сообщение help так:
```
$ python ping_function_ver2.py -h
usage: ping_function_ver2.py [-h] [-c COUNT] host

Ping script

positional arguments:
  host        IP or name to ping

optional arguments:
  -h, --help  show this help message and exit
  -c COUNT    Number of packets
```


