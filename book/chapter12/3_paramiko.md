## Модуль paramiko

Paramiko это реализация протокола SSHv2 на Python. Paramiko предоставляет функциональность клиента и сервера. Мы будем рассматривать только функциональность клиента.

Так как Paramiko не входит в стандартную библиотеку модулей Python, его нужно установить:
```
pip install paramiko
```

Посмотрим сразу на пример использования Paramiko (пример аналогичен тому, который мы использовали в разделах с pexpect и telnetlib).

Скрипт 3_paramiko.py:
```python
import paramiko
import getpass
import sys
import time

COMMAND = sys.argv[1]
USER = raw_input("Username: ")
PASSWORD = getpass.getpass()
ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ')

DEVICES_IP = ['192.168.100.1','192.168.100.2','192.168.100.3']

for IP in DEVICES_IP:
    print "Connection to device %s" % IP
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname=IP, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)
    ssh = client.invoke_shell()

    ssh.send("enable\n")
    ssh.send(ENABLE_PASS + '\n')
    time.sleep(1)

    ssh.send("terminal length 0\n")
    time.sleep(1)
    print ssh.recv(1000)

    ssh.send(COMMAND + "\n")
    time.sleep(2)
    result = ssh.recv(5000)
    print result
```

Разберемся с содержимым скрипта:
* ```client = paramiko.SSHClient()```
 * этот класс представляет соединение к SSH-серверу. Он будет заботиться об аутентификации клиента.
* ```client.set_missing_host_key_policy(paramiko.AutoAddPolicy())```
 * paramiko.AutoAddPolicy() - политика, которая автоматически добавляет новое имя хоста и ключ в локальный объект HostKeys.
 * set_missing_host_key_policy - устанавливает какую политику использовать, когда мы подключаемся к серверу ключ которого неизвестен.
* ```client.connect(IP, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)```
 * client.connect - метод, который выполняет подключение к SSH-серверу и аутентифицирует подключение
    * hostname - имя хоста или IP-адрес
    * username - имя пользователя
    * password - пароль
    * look_for_keys - по умолчанию paramiko выполняет аутентификацию по ключам. Отключаем это поставив False
    * allow_agent - paramiko может подключаться к локальному SSH агенту ОС. Это нужно при работе с ключами, а так как мы выполняем аутентификацию по логину/паролю, лучше это отключить.
 * ```ssh = client.invoke_shell()```
    * После выполнения предыдущей команды у нас уже есть подключение к серверу. Теперь мы вызываем метод invoke_shell, который позволяет нам установить интерактивную сессию SSH с сервером.
 * Внутри установленной сессии мы выполняем команды и получаем, если нужно, вывод:
    * ssh.send - отправляет указанную строку в сессию
    * ssh.recv - получает данные из сессии. В скобках указывается максимальное значение в байтах, которое можно получить. Этот метод возвращает считанную строку
 * Кроме этого, между отправкой команды и считыванием, кое-где стоит строка time.sleep
    * с помощью неё мы указываем паузу - сколько времени подождать, прежде чем скрипт продолжит выполняться. Это мы делаем для того, чтобы дождаться выполнения команды на оборудовании

Так выглядит результат выполнения скрипта:
```
Username: cisco
Password:
Enter enable secret:
Connection to device 192.168.100.1

R1>enable
Password:
R1#terminal length 0


R1#
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
R1#
Connection to device 192.168.100.2

R2>enable
Password:
R2#terminal length 0
R2#
sh ip int br
FastEthernet0/0        192.168.100.2   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.2.10.1       YES manual up                    up
FastEthernet0/1.20     10.2.20.1       YES manual up                    up
FastEthernet0/1.30     10.2.30.1       YES manual up                    up
FastEthernet0/1.40     10.2.40.1       YES manual up                    up
FastEthernet0/1.50     10.2.50.1       YES manual up                    up
FastEthernet0/1.60     10.2.60.1       YES manual up                    up
FastEthernet0/1.70     10.2.70.1       YES manual up                    up
R2#
Connection to device 192.168.100.3

R3>enable
Password:
R3#terminal length 0
R3#
sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.3   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.3.10.1       YES manual up                    up
FastEthernet0/1.20     10.3.20.1       YES manual up                    up
FastEthernet0/1.30     10.3.30.1       YES manual up                    up
FastEthernet0/1.40     10.3.40.1       YES manual up                    up
FastEthernet0/1.50     10.3.50.1       YES manual up                    up
FastEthernet0/1.60     10.3.60.1       YES manual up                    up
FastEthernet0/1.70     10.3.70.1       YES manual up                    up
R3#

```
