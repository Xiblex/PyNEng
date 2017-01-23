## Модуль subprocess

Модуль subprocess позволяет создавать новые процессы.
При этом, он может подключаться к [стандартным потокам ввода/вывода/ошибок](http://xgu.ru/wiki/stdin) и получать код возврата.

> [Документация модуля subprocess](https://docs.python.org/2/library/subprocess.html)

С помощью subprocess, мы можем, например, выполнять любые команды Linux из скрипта.
И, в зависимости от ситуации, получать вывод или только проверять, что команда выполнилась без ошибок.

### Функция ```subprocess.call()```

Функция ```call()```:
* позволяет выполнить команду
 * при этом, она ожидает завершения команды.
* функция возращает код возврата

Попробуем выполнить команду ```ls```:
```python
In [1]: import subprocess

In [2]: result = subprocess.call('ls')
LICENSE.md          course_presentations        faq.md
README.md           course_presentations.zip    howto.md
SUMMARY.md          cover.jpg           images
ToDo.md             examples            resources
about.md            examples.zip            schedule.md
book                exercises
book.json           exercises.zip
```

В переменной result теперь содержится код возврата (код 0 означает, что программа выполнилась успешно):
```python
In [3]: print result
0
```

Обратите внимание, что, если вам нужно вызвать команду с аргументами, её нужно передавать таким образом (как список):
```
In [4]: result = subprocess.call(['ls', '-ls'])
total 3624
   8 -rw-r--r--   1 nata  nata      372 Dec 10 21:34 LICENSE.md
  16 -rw-r--r--   1 nata  nata     4528 Jan 12 09:16 README.md
  32 -rw-r--r--   1 nata  nata    12480 Jan 23 11:15 SUMMARY.md
   8 -rw-r--r--   1 nata  nata     2196 Jan 23 09:16 ToDo.md
   8 -rw-r--r--   1 nata  nata       70 Dec 10 21:34 about.md
   0 drwxr-xr-x  19 nata  nata      646 Jan 23 11:05 book
   8 -rw-r--r--   1 nata  nata      355 Jan 12 09:16 book.json
   0 drwxr-xr-x  16 nata  nata      544 Dec 10 21:34 course_presentations
2176 -rw-r--r--   1 nata  nata  1111234 Dec 10 21:34 course_presentations.zip
 528 -rw-r--r--@  1 nata  nata   267824 Dec 11 08:25 cover.jpg
   0 drwxr-xr-x  20 nata  nata      680 Jan 23 13:05 examples
 360 -rw-r--r--   1 nata  nata   181075 Jan 21 14:10 examples.zip
   0 drwxr-xr-x  19 nata  nata      646 Jan 17 10:24 exercises
 416 -rw-r--r--   1 nata  nata   210621 Jan 21 14:10 exercises.zip
  32 -rw-r--r--   1 nata  nata    14684 Jan 18 05:33 faq.md
  16 -rw-r--r--   1 nata  nata     7043 Jan 17 10:28 howto.md
   0 drwxr-xr-x   4 nata  nata      136 Jan 14 11:01 images
   0 drwxr-xr-x  10 nata  nata      340 Jan 17 08:44 resources
  16 -rw-r--r--@  1 nata  nata     6219 Jan 17 11:37 schedule.md
```

Теперь, попробуем вывести все файлы, с расширением md:
```python
In [5]: result = subprocess.call(['ls', '-ls', '*md'])
ls: *md: No such file or directory
```

Мы получили ошибку.

Чтобы вызывать команды, в которых используются регулярные выражения, нужно добавлять параметр shell:
```python
In [6]: result = subprocess.call(['ls', '-ls', '*md'], shell=True)
LICENSE.md          course_presentations        faq.md
README.md           course_presentations.zip    howto.md
SUMMARY.md          cover.jpg           images
ToDo.md             examples            resources
about.md            examples.zip            schedule.md
book                exercises
book.json           exercises.zip
```

Когда мы устанавливаем ```shell=True```, указанная команда выполняется через shell.
В таком случае, мы можем передавать команду так:
```python
In [7]: result = subprocess.call('ls -ls *md', shell=True)
 8 -rw-r--r--  1 nata  nata    372 Dec 10 21:34 LICENSE.md
16 -rw-r--r--  1 nata  nata   4528 Jan 12 09:16 README.md
32 -rw-r--r--  1 nata  nata  12480 Jan 23 11:15 SUMMARY.md
 8 -rw-r--r--  1 nata  nata   2196 Jan 23 09:16 ToDo.md
 8 -rw-r--r--  1 nata  nata     70 Dec 10 21:34 about.md
32 -rw-r--r--  1 nata  nata  14684 Jan 18 05:33 faq.md
16 -rw-r--r--  1 nata  nata   7043 Jan 17 10:28 howto.md
16 -rw-r--r--@ 1 nata  nata   6219 Jan 17 11:37 schedule.md
```

Ещё одна особенность функции ```call()``` - она ожидает завершения выполнения команды.
Если попробовать, например, запустить команду ping, то этот аспект будет заметен:
```python
In [8]: reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'])
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.868 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.243 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=50.029 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.243/49.713/50.029/0.339 ms
```

Особенно, если вы попробуете пингануть какой-то недоступный IP-адрес.

Итак, функция ```call()``` подходит, если вам нужно:
* подождать выполнения программы, прежде чем выполнять следующие шаги
* нужно получить только код выполнения и не нужен вывод

Ещё один аспект работы функции ``call()```, который вы наверняка заметили, она выводит результат выполнения команды, на стандартный поток вывода.

Если мы сделаем такой скрипт (файл subprocess_call.py):
```python
import subprocess

reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'])

if reply == 0:
    print "Alive"
else:
    print "Unreachable"
```

Результат выполнения будет таким:
```
$ python subprocess_call.py
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.930 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=48.981 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=48.360 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.360/49.090/49.930/0.646 ms
Alive
```

То есть, результат выполнения команды, выводится на стандартный поток вывода нашего скрипта.

Если нужно это отключить и не выводить результат выполнения, надо перенаправить stdout в devnull (файл subprocess_call_devnull.py):
```python
import subprocess
import os

DNULL = open(os.devnull, 'w')

reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'], stdout=DNULL)

if reply == 0:
    print "Alive"
else:
    print "Unreachable"
```

Теперь результат выполнения будет таким:
```
$ python subprocess_call_devnull.py
Alive
```

### Функция ```subprocess.check_output()```

Функция ```check_output()```:
* позволяет выполнить команду
 * при этом, она ожидает завершения команды.
* если команда отработала корректно (код возврата 0), функция возращает результат выполнения команды
* если возникла ошибка, при выполнении команды, функция генерирует исключение

Пример использования функции ```check_output()``` (файл subprocess_check_output.py):
```python
import subprocess

reply = subprocess.check_output(['ping', '-c', '3', '-n', '8.8.8.8'])

print "Result:"
print reply
```

Результат выполнения (если убрать строку ```print reply```, на стандартный поток вывода ничего не будет выведено):
```
$ python subprocess_check_output.py
Result:
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.785 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=57.231 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=51.071 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.785/52.696/57.231/3.250 ms
```

Теперь попробуем выполнить команду, в которой код возрата будет не 0 (команду с ошибкой).
Для этого, просто напишем, вместо адреса, какой-то символ (файл subprocess_check_output_catch_exception.py):
```python
$ python subprocess_check_output_catch_exception.py
ping: cannot resolve a: Unknown host
Traceback (most recent call last):
  File "subprocess_check_output_catch_exception.py", line 3, in <module>
    reply = subprocess.check_output(['ping', '-c', '3', '-n', 'a'])
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 573, in check_output
    raise CalledProcessError(retcode, cmd, output=output)
subprocess.CalledProcessError: Command '['ping', '-c', '3', '-n', 'a']' returned non-zero exit status 68
```

Мы получили исключение ```CalledProcessError``` и соответствующее сообщение об ошибке.
Функция ```check_output()``` всегда будет возвращать это исключение, когда код возврата не равен 0.

Это значит, что мы можем написать выражение try/except, с помощью которого будем проверять корректно ли отработала команда (дополняем файл subprocess_check_output_catch_exception.py):
```python
import subprocess

try:
    reply = subprocess.check_output(['ping', '-c', '3', '-n', 'a'])
except subprocess.CalledProcessError as e:
    print "Error occurred"
    print "Return code:", e.returncode
```

Результат выполнения:
```
$ python subprocess_check_output_catch_exception.py
ping: cannot resolve a: Unknown host
Error occurred
Return code: 68
```

Теперь мы увидели сообщение об ошибке и код возврата и программа завершилась корректно.
Но, само сообщение об ошибке, попало на стандартный поток вывода, хотя мы его не выводили.

Попробуем собрать всё в финальную функцию и добавим перехват сообщения об ошибке:
```python
import subprocess
from tempfile import TemporaryFile


def ping_ip(ip_address):
    """
    Ping IP address and return tuple:
    On success:
        * return code = 0
        * command output
    On failure:
        * return code
        * error output (stderr)
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', '3', '-n', ip_address],
                                             stderr=temp)
            return 0, output
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read()

print ping_ip('8.8.8.8')
print ping_ip('a')
```

Результат выполнения будет таким:
```
$ python subprocess_ping_function.py
(0, 'PING 8.8.8.8 (8.8.8.8): 56 data bytes\n64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=46.106 ms\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=46.114 ms\n64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=47.390 ms\n\n--- 8.8.8.8 ping statistics ---\n3 packets transmitted, 3 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 46.106/46.537/47.390/0.603 ms\n')

(68, 'ping: cannot resolve a: Unknown host\n')
```

> В примере использованы идеи из [ответа на stackoverflow](http://stackoverflow.com/questions/30937829/how-to-get-both-return-code-and-output-from-subprocess-in-python/30937898#30937898)

Модуль tempfile входит в стандартную библиотеку Python и используется тут для того, чтобы сохранить сообщение об ошибке.
Мы используем функцию TemporaryFile, которая создает временный файл и удаляет его автоматически, после того, как файл закрывается.

> Подробнее о модуле tempfile можно почитать на сайте [PyMOTW](https://pymotw.com/2/tempfile/).


