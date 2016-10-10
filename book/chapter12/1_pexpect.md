## Модуль pexpect

Для начала, модуль pexpect нужно установить:
```
pip install pexpect
```

Модуль pexpect позволяет автоматизировать интерактивные подключения, такие как:
* telnet
* ssh
* ftp

> Pexpect это реализация expect на Python.

Логика работы pexpect такая:
* запускаем какую-то программу
* ожидаем определенный вывод (приглашение, запрос пароля и подобное)
* отправляем команды/данные
* последние два действия повторяются столько, сколько нужно

Очень важно понимать, что сам pexpect не реализует различные утилиты, а использует уже готовые.

В Pexpect есть два основных инструмента:
* функция run()
* класс spawn

### pexpect.run()

Функция run() позволяет легко вызвать какую-то программу и вернуть её вывод.

Например:
```python
In [1]: import pexpect

In [2]: output = pexpect.run('ls -ls')

In [3]: print output
total 368
  8 -rw-r--r--   1 natasha  staff     372 Sep 26 08:36 LICENSE.md
  8 -rw-r--r--   1 natasha  staff    3483 Sep 26 08:36 README.md
 16 -rw-r--r--   1 natasha  staff    7098 Oct  5 11:41 SUMMARY.md
  8 -rw-r--r--   1 natasha  staff      70 Sep 25 19:01 about.md
  0 drwxr-xr-x  17 natasha  staff     578 Sep 25 19:05 book
  8 -rw-r--r--   1 natasha  staff     239 Sep 27 06:32 book.json
288 -rw-r--r--   1 natasha  staff  146490 Sep 27 09:11 cover.jpg
  0 drwxr-xr-x   6 natasha  staff     204 Sep 25 19:01 exercises
 24 -rw-r--r--   1 natasha  staff   10024 Sep 25 19:01 faq.md
  0 drwxr-xr-x   3 natasha  staff     102 Sep 27 16:25 resources
  8 -rw-r--r--   1 natasha  staff    3633 Sep 27 15:52 schedule.md
```

### pexpect.spawn

Класс spawn поддерживает больше возможностей. Он позволяет взаимодействовать с вызванной программой, отправляя данные и ожидая ответ.

Простой пример использования pexpect.spwan:
```python
t = pexpect.spawn('ssh user@10.1.1.1')

t.expect('Password:')
t.sendline("userpass")
t.expect('>')
```

Тут мы подключаемся по SSH, и ожидаем строку 'Password:'. Как только она появилась, отправляем пароль. Затем ждем строку '>'.


### Пример использования pexpect
Посмотрим на еще один пример использования pexpect, теперь уже чуть более сложный.

Файл 1_pexpect.py:
```python
import pexpect
import getpass
import sys

COMMAND = sys.argv[1]
USER = raw_input("Username: ")
PASSWORD = getpass.getpass()
ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ')

DEVICES_IP = ['192.168.100.1','192.168.100.2','192.168.100.3']

for IP in DEVICES_IP:
    print "Connection to device %s" % IP
    t = pexpect.spawn('ssh %s@%s' % (USER, IP))

    t.expect('Password:')
    t.sendline(PASSWORD)

    t.expect('>')
    t.sendline('enable')

    t.expect('Password:')
    t.sendline(ENABLE_PASS)

    t.expect('#')
    t.sendline("terminal length 0")

    t.expect('#')
    t.sendline(COMMAND)

    t.expect('#')
    print t.before

```

В этом скрипте:
* мы ожидаем, что скрипту будет передан аргумент - этот аргумент указывает какую команду выполнить на устройствах
* затем мы запрашиваем логин, пароль и пароль на режим enable
 * пароли мы запрашиваем используя модуль getpass
* ip_list это список IP-адресов устройств, к которым мы будем подключаться
* затем мы проходимся в цикле по адресам и подключаемся по очереди к устройствам
* в классе spawn мы запускаем ssh к текущему адресу, подставляя сразу имя пользователя
* затем у нас идут пары: expect и sendline
 * мы ждем появления определенной подстроки (expect)
 * когда строка появилась, отправляем команду (sendline)
* так происходит до конца цикла, и только последняя команда отличается:
 * before позволяет считать всё, что поймал pexpect до предыдущей подстроки в expect

Попробуем запустить скрипт:
```python
natasha@nattaur: $ python 1_pexpect.py "sh ip int br"
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

Обратите внимание, что, так как мы в последнем expect ожидали подстроку ```#```, метод before показал и команду и имя хоста.

> На самом деле, before это атрибут класса, но пока что, слово метод будет понятней.


###Специальные символы в shell

Pexpect не интерпретирует специальные символы shell, такие как ```>```, ```|```, ```*```.

Для того чтобы, например, команда ```ls -ls | grep SUMMARY``` отработала, нужно запустить shell таким образом:
```python
In [1]: import pexpect

In [2]: p = pexpect.spawn('/bin/bash -c "ls -ls | grep SUMMARY"')

In [3]: p.expect(pexpect.EOF)
Out[3]: 0

In [4]: print p.before
 16 -rw-r--r--   1 natasha  staff    7156 Oct  5 13:05 SUMMARY.md
```

#### pexpect.EOF
В предыдущем примере встретилось использование pexpect.EOF.

Это специальное значение, которое позволяет отреагировать на завершенние исполнения команды или сессии, которую мы запустили в spawn.

Когда мы запускаем команду ```ls -ls```, мы не получаем интерактивный сеанс. Команда выполняется и всё, на этом завершается её работа.

Поэтому, если бы мы попытались запустить её и указать в expect приглашение, мы бы получили ошибку:
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

EOF: End Of File (EOF). Empty string style platform.
<pexpect.pty_spawn.spawn object at 0x107100b10>
command: /bin/bash
args: ['/bin/bash', '-c', 'ls -ls | grep SUMMARY']
searcher: None
buffer (last 100 chars): ''
before (last 100 chars): ' 16 -rw-r--r--   1 natasha  staff    7156 Oct  5 13:05 SUMMARY.md\r\n'
after: <class 'pexpect.exceptions.EOF'>
match: None
match_index: None
exitstatus: 0
flag_eof: True
pid: 85765
child_fd: 7
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
```

Когда мы передаем в expect EOF, мы не получаем эту ошибку.

###Возможности pexpect.expect

pexpect.expect в качестве шаблона может принимать не только строку. Выше, мы уже встретились с вариантом передачи EOF.

Что может использоваться как шаблон в pexpect/expect:
* строка
* EOF - этот шаблон позволяет среагировать на исключение EOF
* TIMEOUT - исключение timeout (по умолчанию значение timeout = 30 секунд)
* compiled re

Еще одна очень полезная возможность pexpect.expect: то, что мы можем передевать не одно значение, а список.

Например:
```python
In [7]: p = pexpect.spawn('/bin/bash -c "ls -ls | grep SUMMARY"')

In [8]: p.expect(['nattaur', pexpect.TIMEOUT, pexpect.EOF])
Out[8]: 2
```

Тут несколько важных моментов:
* когда мы вызываем pexpect.expect со списком, мы можем указывать разные ожидаемые строки
* кроме строк, можно указывать исключения
* pexpect.expect возвращает номер элемента списка, который сработал
 * в данном случае, номер 2, так как исключение EOF находится в списке под номером два
* засчет такого формата, мы можем делать ответвления в программе и говорить, если совпадение с первым элементом, то сделать одни действия, если со вторым - другие и так далее.


###Документация pexpect
На этом мы завершаем рассмотрение модуля pexpect. Документация модуля: [pexpect](https://pexpect.readthedocs.io/en/stable/index.html).
