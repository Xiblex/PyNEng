## Примеры конвертации между байтами и строками

Рассмотрим несколько примеров работы с байтами и конвертации байт в строки.


### subprocess

Модуль subprocess возвращает результат команды в виде байт:
```python
In [1]: import subprocess

In [2]: result = subprocess.run(['ping', '-c', '3', '-n', '8.8.8.8'],
   ...:                         stdout=subprocess.PIPE)
   ...:

In [4]: result.stdout
Out[4]: b'PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=43 time=59.4 ms\n64 bytes from 8.8.8.8: icmp_seq=2 ttl=43 time=54.4 ms\n64 bytes from 8.8.8.8: icmp_seq=3 ttl=43 time=55.1 ms\n\n--- 8.8.8.8 ping statistics ---\n3 packets transmitted, 3 received, 0% packet loss, time 2002ms\nrtt min/avg/max/mdev = 54.470/56.346/59.440/2.220 ms\n'
```

Если дальше необходимо работать с этим выводом, надо сразу конвертировать его в строку:
```python
In [7]: output = result.stdout.decode('utf-8')

In [8]: print(output)
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=43 time=59.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=43 time=54.4 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=43 time=55.1 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 54.470/56.346/59.440/2.220 ms
```

Модуль subprocess поддерживает еще один вариант преобразования - параметр encoding.
Если указать его при вызове функции run, результат будет получен в виде строки:
```python
In [10]: result = subprocess.run(['ping', '-c', '3', '-n', '8.8.8.8'],
    ...:                         stdout=subprocess.PIPE, encoding='utf-8')
    ...:

In [11]: result.stdout
Out[11]: 'PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=43 time=55.5 ms\n64 bytes from 8.8.8.8: icmp_seq=2 ttl=43 time=54.6 ms\n64 bytes from 8.8.8.8: icmp_seq=3 ttl=43 time=53.3 ms\n\n--- 8.8.8.8 ping statistics ---\n3 packets transmitted, 3 received, 0% packet loss, time 2003ms\nrtt min/avg/max/mdev = 53.368/54.534/55.564/0.941 ms\n'

In [12]: print(result.stdout)
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=43 time=55.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=43 time=54.6 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=43 time=53.3 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 53.368/54.534/55.564/0.941 ms
```

### telnetlib

В зависимости от модуля, преобразование между строками и байтами может выполняться автоматически, а может требоваться явно.

Например, в модуле telnetlib необходимо передавать байты в методах read_until и write:
```python
import telnetlib
import time
 
t = telnetlib.Telnet('192.168.100.1')
 
t.read_until(b'Username:')
t.write(b'cisco\n')
 
t.read_until(b'Password:')
t.write(b'cisco\n')
t.write(b'sh ip int br\n')
 
time.sleep(5)
 
output = t.read_very_eager().decode('utf-8')
print(output)
```

И возвращает метод байты, поэтому в предпоследней строке используется decode.

### pexpect

Модуль pexpect как аргумент ожидает строку, а возвращает байты:
```python
In [26]: import pexpect

In [27]: output = pexpect.run('ls -ls')

In [28]: output
Out[28]: b'total 8\r\n4 drwxr-xr-x 2 vagrant vagrant 4096 Aug 28 12:16 concurrent_futures\r\n4 drwxr-xr-x 2 vagrant vagrant 4096 Aug  3 07:59 iterator_generator\r\n'

In [29]: output.decode('utf-8')
Out[29]: 'total 8\r\n4 drwxr-xr-x 2 vagrant vagrant 4096 Aug 28 12:16 concurrent_futures\r\n4 drwxr-xr-x 2 vagrant vagrant 4096 Aug  3 07:59 iterator_generator\r\n'
```

И также поддерживает вариант передачи кодировки через параметр encoding:
```python
In [30]: output = pexpect.run('ls -ls', encoding='utf-8')

In [31]: output
Out[31]: 'total 8\r\n4 drwxr-xr-x 2 vagrant vagrant 4096 Aug 28 12:16 concurrent_futures\r\n4 drwxr-xr-x 2 vagrant vagrant 4096 Aug  3 07:59 iterator_generator\r\n'
```

### Выводы

Эти примеры показаны тут для того, чтобы показать, что разные модули могут по-разному подходить к вопросу конвертации между строками и байтами.
И разные функции и методы этих модулей могут ожидать аргументы и возвращать значения разных типов.
Однако все эти вещи написаны в документации.

