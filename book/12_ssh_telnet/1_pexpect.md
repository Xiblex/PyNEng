## Модуль pexpect

Модуль pexpect позволяет автоматизировать интерактивные подключения, такие как:
* telnet
* ssh
* ftp

Для начала, модуль pexpect нужно установить:
```
pip install pexpect
```

> Pexpect это реализация expect на Python.

Логика работы pexpect такая:
* запускается какая-то программа
* pexpect ожидает определенный вывод (приглашение, запрос пароля и подобное)
* получив вывод, он отправляет команды/данные
* последние два действия повторяются столько, сколько нужно

При этом, сам pexpect не реализует различные утилиты, а использует уже готовые.

В pexpect есть два основных инструмента:
* функция ```run()```
* класс ```spawn```

### ```pexpect.run()```

Функция ```run()``` позволяет легко вызвать какую-то программу и вернуть её вывод.

Например:
```python
In [1]: import pexpect

In [2]: output = pexpect.run('ls -ls')

In [3]: print(output)
b'total 44\r\n4 -rw-r--r-- 1 vagrant vagrant 3203 Jul 14 07:15 1_pexpect.py\r\n4 -rw-r--r-- 1 vagrant vagrant 3393 Jul 14 07:15 2_telnetlib.py\r\n4 -rw-r--r-- 1 vagrant vagrant 3452 Jul 14 07:15 3_paramiko.py\r\n4 -rw-r--r-- 1 vagrant vagrant 3127 Jul 14 07:15 4_netmiko.py\r\n4 -rw-r--r-- 1 vagrant vagrant  718 Jul 14 07:15 4_netmiko_telnet.py\r\n4 -rw-r--r-- 1 vagrant vagrant  300 Jul  8 15:31 devices.yaml\r\n4 -rw-r--r-- 1 vagrant vagrant  413 Jul 14 07:15 netmiko_function.py\r\n4 -rw-r--r-- 1 vagrant vagrant  876 Jul 14 07:15 netmiko_multiprocessing.py\r\n4 -rw-r--r-- 1 vagrant vagrant 1147 Jul 14 07:15 netmiko_threading_data_list.py\r\n4 -rw-r--r-- 1 vagrant vagrant 1121 Jul 14 07:15 netmiko_threading_data.py\r\n4 -rw-r--r-- 1 vagrant vagrant  671 Jul 14 07:15 netmiko_threading.py\r\n'

In [4]: print(output.decode('utf-8'))
total 44
4 -rw-r--r-- 1 vagrant vagrant 3203 Jul 14 07:15 1_pexpect.py
4 -rw-r--r-- 1 vagrant vagrant 3393 Jul 14 07:15 2_telnetlib.py
4 -rw-r--r-- 1 vagrant vagrant 3452 Jul 14 07:15 3_paramiko.py
4 -rw-r--r-- 1 vagrant vagrant 3127 Jul 14 07:15 4_netmiko.py
4 -rw-r--r-- 1 vagrant vagrant  718 Jul 14 07:15 4_netmiko_telnet.py
4 -rw-r--r-- 1 vagrant vagrant  300 Jul  8 15:31 devices.yaml
4 -rw-r--r-- 1 vagrant vagrant  413 Jul 14 07:15 netmiko_function.py
4 -rw-r--r-- 1 vagrant vagrant  876 Jul 14 07:15 netmiko_multiprocessing.py
4 -rw-r--r-- 1 vagrant vagrant 1147 Jul 14 07:15 netmiko_threading_data_list.py
4 -rw-r--r-- 1 vagrant vagrant 1121 Jul 14 07:15 netmiko_threading_data.py
4 -rw-r--r-- 1 vagrant vagrant  671 Jul 14 07:15 netmiko_threading.py

```

### ```pexpect.spawn```

Класс ```spawn``` поддерживает больше возможностей. Он позволяет взаимодействовать с вызванной программой, отправляя данные и ожидая ответ.

Простой пример использования pexpect.spawn:
```python
t = pexpect.spawn('ssh user@10.1.1.1')

t.expect('Password:')
t.sendline('userpass')
t.expect('>')
```

Сначала выполняется подключение по SSH, затем pexpect ожидает строку ```Password:```.
Как только эта строка появилась, отправляется пароль.
После отправки, pexpect ожидает строку ```>```.


### Пример использования pexpect

Пример использования pexpect для подключения к оборудованию и передачи команды show (файл 1_pexpect.py):
```python
import pexpect
import getpass
import sys

COMMAND = sys.argv[1]
USER = input('Username: ')
PASSWORD = getpass.getpass()
ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ')

DEVICES_IP = ['192.168.100.1','192.168.100.2','192.168.100.3']

for IP in DEVICES_IP:
    print('Connection to device {}'.format(IP))
    with pexpect.spawn('ssh {}@{}'.format(USER, IP)) as ssh:

        ssh.expect('Password:')
        ssh.sendline(PASSWORD)

        ssh.expect('[#>]')
        ssh.sendline('enable')

        ssh.expect('Password:')
        ssh.sendline(ENABLE_PASS)

        ssh.expect('#')
        ssh.sendline('terminal length 0')

        ssh.expect('#')
        ssh.sendline(COMMAND)

        ssh.expect('#')
        print(ssh.before.decode('utf-8'))

```

Комментарии с скрипту:
* команда, которую нужно выполнить, передается как аргумент
* затем запрашивается логин, пароль и пароль на режим enable
 * пароли запрашиваются с помощью модуля getpass
* ```ip_list``` это список IP-адресов устройств, к которым будет выполняться подключение
* в цикле, выполняется подключение к устройствам из списка
* в классе spawn выполняется подключение по SSH к текущему адресу, используя указанное имя пользователя
* после этого, начинают чередоваться пары методов: expect и sendline
 * ```expect``` - ожидание подстроки
 * ```sendline``` - когда строка появилась, отправляется команда
* так происходит до конца цикла, и только последняя команда отличается:
 * ```before``` позволяет считать всё, что поймал pexpect до предыдущей подстроки в expect

Обратите внимание на строку ```ssh.expect('[#>]')```.
Метод expect ожидает не просто строку, а регулярное выражение.

Выполнение скрипта выглядит так:
```python
$ python 1_pexpect.py "sh ip int br"
Username: nata
Password:
Enter enable secret:
Connection to device 192.168.100.1
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.1   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.1.10.1       YES manual up                    up
FastEthernet0/1.20     10.1.20.1       YES manual up                    up
FastEthernet0/1.30     10.1.30.1       YES manual up                    up
FastEthernet0/1.40     10.1.40.1       YES manual up                    up
FastEthernet0/1.50     10.1.50.1       YES manual up                    up
FastEthernet0/1.60     10.1.60.1       YES manual up                    up
FastEthernet0/1.70     10.1.70.1       YES manual up                    up
R1
Connection to device 192.168.100.2
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.2   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.2.10.1       YES manual up                    up
FastEthernet0/1.20     10.2.20.1       YES manual up                    up
FastEthernet0/1.30     10.2.30.1       YES manual up                    up
FastEthernet0/1.40     10.2.40.1       YES manual up                    up
FastEthernet0/1.50     10.2.50.1       YES manual up                    up
FastEthernet0/1.60     10.2.60.1       YES manual up                    up
FastEthernet0/1.70     10.2.70.1       YES manual up                    up
R2
Connection to device 192.168.100.3
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.3   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.3.10.1       YES manual up                    up
FastEthernet0/1.20     10.3.20.1       YES manual up                    up
FastEthernet0/1.30     10.3.30.1       YES manual up                    up
FastEthernet0/1.40     10.3.40.1       YES manual up                    up
FastEthernet0/1.50     10.3.50.1       YES manual up                    up
FastEthernet0/1.60     10.3.60.1       YES manual up                    up
FastEthernet0/1.70     10.3.70.1       YES manual up                    up
R3
```

Обратите внимание, что, так как в последнем expect указано, что надо ожидать подстроку ```#```, метод before показал и команду и имя хоста.


###Специальные символы в shell

Pexpect не интерпретирует специальные символы shell, такие как ```>```, ```|```, ```*```.

Для того чтобы, например, команда ```ls -ls | grep SUMMARY``` отработала, нужно запустить shell таким образом:
```python
In [1]: import pexpect

In [2]: p = pexpect.spawn('/bin/bash -c "ls -ls | grep pexpect"')

In [3]: p.expect(pexpect.EOF)
Out[3]: 0

In [4]: print(p.before)
b'4 -rw-r--r-- 1 vagrant vagrant 3203 Jul 14 07:15 1_pexpect.py\r\n'

In [5]: print(p.before.decode('utf-8'))
4 -rw-r--r-- 1 vagrant vagrant 3203 Jul 14 07:15 1_pexpect.py

```

#### pexpect.EOF
В предыдущем примере встретилось использование pexpect.EOF.

> EOF (end of file) — конец файла

Это специальное значение, которое позволяет отреагировать на завершенние исполнения команды или сессии, которая была запущена в spawn.

При вызове команды ```ls -ls```, pexpect не получает интерактивный сеанс.
Команда выполняется и всё, на этом завершается её работа.

Поэтому, если запустить её и указать в expect приглашение, возникнет ошибка:
```python
In [5]: p = pexpect.spawn('/bin/bash -c "ls -ls | grep SUMMARY"')

In [6]: p.expect('nattaur')
---------------------------------------------------------------------------
EOF                                       Traceback (most recent call last)
<ipython-input-9-9c71777698c2> in <module>()
----> 1 p.expect('nattaur')

/Library/Python/2.7/site-packages/pexpect/spawnbase.pyc in expect(self, pattern, timeout, searchwindowsize, async)
    313         compiled_pattern_list = self.compile_pattern_list(pattern)
    314         return self.expect_list(compiled_pattern_list,
--> 315                 timeout, searchwindowsize, async)
    316
    317     def expect_list(self, pattern_list, timeout=-1, searchwindowsize=-1,

/Library/Python/2.7/site-packages/pexpect/spawnbase.pyc in expect_list(self, pattern_list, timeout, searchwindowsize, async)
    337             return expect_async(exp, timeout)
    338         else:
--> 339             return exp.expect_loop(timeout)
    340
    341     def expect_exact(self, pattern_list, timeout=-1, searchwindowsize=-1,

/Library/Python/2.7/site-packages/pexpect/expect.pyc in expect_loop(self, timeout)
    100                     timeout = end_time - time.time()
    101         except EOF as e:
--> 102             return self.eof(e)
    103         except TIMEOUT as e:
    104             return self.timeout(e)

/Library/Python/2.7/site-packages/pexpect/expect.pyc in eof(self, err)
     47             if err is not None:
     48                 msg = str(err) + '\n' + msg
---> 49             raise EOF(msg)
     50
     51     def timeout(self, err=None):

EOF: End Of File (EOF). Exception style platform.
<pexpect.pty_spawn.spawn object at 0xb4f7366c>
command: /bin/bash
args: ['/bin/bash', '-c', 'ls -ls | grep pexpect']
buffer (last 100 chars): b''
before (last 100 chars): b'4 -rw-r--r-- 1 vagrant vagrant 3203 Jul 14 07:15 1_pexpect.py\r\n'
after: <class 'pexpect.exceptions.EOF'>
match: None
match_index: None
exitstatus: 0
flag_eof: True
pid: 3189
child_fd: 16
closed: False
timeout: 30
delimiter: <class 'pexpect.exceptions.EOF'>
logfile: None
logfile_read: None
logfile_send: None
maxread: 2000
ignorecase: False
searchwindowsize: None
delaybeforesend: 0.05
delayafterclose: 0.1
delayafterterminate: 0.1
searcher: searcher_re:
    0: re.compile("b'py3_convert'")

```

Но, если передать в expect EOF, ошибки не будет.

### Возможности pexpect.expect

```pexpect.expect``` в качестве шаблона может принимать не только строку.


Что может использоваться как шаблон в pexpect.expect:
* строка
* EOF - этот шаблон позволяет среагировать на исключение EOF
* TIMEOUT - исключение timeout (по умолчанию значение timeout = 30 секунд)
* compiled re

Еще одна очень полезная возможность pexpect.expect: можно передавать не одно значение, а список.

Например:
```python
In [7]: p = pexpect.spawn('/bin/bash -c "ls -ls | grep netmiko"')

In [8]: p.expect(['py3_convert', pexpect.TIMEOUT, pexpect.EOF])
Out[8]: 2

```

Тут несколько важных моментов:
* когда pexpect.expect вызывается со списком, можно указывать разные ожидаемые строки
* кроме строк, можно указывать исключения
* pexpect.expect возвращает номер элемента списка, который сработал
 * в данном случае, номер 2, так как исключение EOF находится в списке под номером два
* за счет такого формата, можно делать ответвления в программе, в зависимости от того с каким элементом было совпадение

