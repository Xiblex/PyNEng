## Конфигурационный файл

Настройки Ansible можно менять в конфигурационном файле.

Конфигурационный файл Ansible может хранится в разных местах (файлы перечислены в порядке уменьшения приоритетности):
* ANSIBLE_CONFIG (переменная окружения)
* ansible.cfg (в текущем каталоге)
* .ansible.cfg (в домашнем каталоге пользователя)
* /etc/ansible/ansible.cfg

Ansible ищет файл конфигурации в указанном порядке и использует первый найденный (конфигурация из разных файлов не совмещается).

В конфигурационном файле можно менять множество параметров. Мы разберем лишь несколько. Остальные параметры и их описание, можно найти в [документации](http://docs.ansible.com/ansible/intro_configuration.html).

В текущем каталоге у вас уже должен быть инвентарный файл myhosts:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100
```

Теперь создадим в локальном каталоге конфигурационный файл ansible.cfg:
```
[defaults]

inventory = ./myhosts
remote_user = cisco
ask_pass = True
```

Разберемся с настройками в конфигурационном файле:
* ```[defaults]``` - это секция конфигурации описывает общие параметры по умолчанию
* ```inventory = ./myhosts``` - параметр inventory позволяет указать местоположение инвентарного файла.
 * Если настроить этот параметр, то нам не придется указывать, где находится файл, каждый раз когда мы запускаем Ansible
* ```remote_user = cisco``` - от имени какого пользователя будет подключаться Ansible
* ```ask_pass = True``` - этот параметр аналогичен опции --ask-pass в командной строке. Если он выставлен в конфигурации Ansible, то уже не нужно указывать его в командной строке.

Теперь вызов ad-hoc команды будет выглядеть так:
```
$ ansible cisco-routers -m raw -a "sh ip int br"
```

То есть, нам не нужно указывать инвентарный файл, пользователя и опцию --ask-pass.


###host_key_checking

Ещё одна настройка, которая может пригодится - host_key_checking.
Она полезна в том случае, когда в управляющего хоста Ansible вы подключаетесь первый раз к большому количеству устройств.

Если указать в конфигурационном файле ```host_key_checking=False```,  будет отключена проверка ключей, при подключении по SSH.

Чтобы проверить этот функционал, удалим сохраненные ключи для устройств Cisco, к которым мы подключаемся.
Для этого, нужно удалить ключи, которые соответствуют этим устройствам из файла ~/.ssh/known_hosts.

Теперь, если мы запустим ad-hoc команду, мы получим такой вывод:
```
$ ansible cisco-routers -m raw -a "sh ip int br"
SSH password:
192.168.100.1 | FAILED | rc=0 >>
Using a SSH password instead of a key is not possible because Host Key checking is enabled and sshpass does not support this.  Please add this host's fingerprint to your known_hosts file to manage this host.

192.168.100.2 | FAILED | rc=0 >>
Using a SSH password instead of a key is not possible because Host Key checking is enabled and sshpass does not support this.  Please add this host's fingerprint to your known_hosts file to manage this host.

192.168.100.3 | FAILED | rc=0 >>
Using a SSH password instead of a key is not possible because Host Key checking is enabled and sshpass does not support this.  Please add this host's fingerprint to your known_hosts file to manage this host.
```

Теперь добавим в конфигурационный файл параметр host_key_checking:
```
[defaults]

inventory = ./myhosts

remote_user = cisco
ask_pass = True

host_key_checking=False
```

И повторим ad-hoc команду:
```
$ ansible cisco-routers -m raw -a "sh ip int br"
SSH password:
192.168.100.1 | SUCCESS | rc=0 >>

Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
Ethernet0/2                unassigned      YES NVRAM  administratively down down
Ethernet0/3                unassigned      YES NVRAM  administratively down down    Warning: Permanently added '192.168.100.1' (RSA) to the list of known hosts.
Connection to 192.168.100.1 closed by remote host.
Shared connection to 192.168.100.1 closed.


192.168.100.2 | SUCCESS | rc=0 >>

Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES manual up                    up
Ethernet0/1                unassigned      YES unset  administratively down down
Ethernet0/2                unassigned      YES unset  administratively down down
Ethernet0/3                unassigned      YES unset  administratively down down    Warning: Permanently added '192.168.100.2' (RSA) to the list of known hosts.
Shared connection to 192.168.100.2 closed.


192.168.100.3 | SUCCESS | rc=0 >>

Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES manual up                    up
Ethernet0/1                unassigned      YES unset  administratively down down
Ethernet0/2                unassigned      YES unset  administratively down down
Ethernet0/3                unassigned      YES unset  administratively down down    Warning: Permanently added '192.168.100.3' (RSA) to the list of known hosts.
Shared connection to 192.168.100.3 closed.
```

Обратите внимание на строки:
```
 Warning: Permanently added '192.168.100.1' (RSA) to the list of known hosts.
```

Это Ansible сам добавил ключи устройств в файл ~/.ssh/known_hosts.
При подключении в следующий раз этого сообщения уже не будет.

На этом мы завершаем знакомство с конфигурационном файлом Ansible.
Другие параметры вы можете посмотреть в документации.
И можно посмотреть на пример конфигурационного файла в [репозитории Ansible](https://github.com/ansible/ansible/blob/devel/examples/ansible.cfg).


