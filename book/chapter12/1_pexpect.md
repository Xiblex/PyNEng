## Модуль pexpect

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

Посмотрим на еще один пример использования pexpect, теперь уже чуть более сложный.

Файл 1_pexpect.py:
```python
import pexpect
import getpass
import sys

command = sys.argv[1]
user = raw_input("Username: ")
password = getpass.getpass()
enable_pass = getpass.getpass(prompt='Enter enable secret: ')

ip_list = ['192.168.100.1','192.168.100.2','192.168.100.3']

for ip in ip_list:
    print "Connection to device %s" % ip
    t = pexpect.spawn('ssh %s@%s' % (user, ip))

    t.expect('Password:')
    t.sendline(password)

    t.expect('>')
    t.sendline('enable')

    t.expect('Password:')
    t.sendline(enable_pass)

    t.expect('#')
    t.sendline("terminal length 0")

    t.expect('#')
    t.sendline(command)

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
