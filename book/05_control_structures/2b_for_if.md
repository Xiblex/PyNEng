### Совмещение for и if
На примере выше стало понятно, что в настройках не хватает добавления порта  в определенный VLAN.

Добавим эту возможность.

Соответственно, в списке, в котором хранились команды, добавилась еще одна команда и в ней не хватает только номера VLAN.

Вместо списка интерфейсов, теперь мы используем словарь.

В словаре будет две категории интерфейсов: access и trunk (пока что только access).
В словаре fast_int по ключу access также находится словарь, в котором ключ - это номер интерфейса, а значение - это номер VLAN.

Файл generate_access_port_config.py выглядит так:
```python
access_template = ['switchport mode access', 'switchport access vlan', 'spanning-tree portfast', 'spanning-tree bpduguard enable']

fast_int = {'access':{'0/12':'10','0/14':'11','0/16':'17','0/17':'150'}}

for intf in fast_int['access']:
    print 'interface FastEthernet' + intf
    for command in access_template:
        if command.endswith('access vlan'):
            print ' %s %s' % (command, fast_int['access'][intf])
        else:
            print ' %s' % command
```

Комментарии к коду:
* В первом цикле for мы перебираем ключи во вложенном словаре fast_int['access']
* Ключ, который мы берем на данный момент цикла, будет храниться в переменной int
* Как и в прошлом примере печатаем строку interface FastEthernet и добавляем к ней номер интерфейса
* Во втором цикле for мы перебираем команды из списка access_template
* Но, так как теперь надо надо добавить номер VLAN к команде switchport access vlan:
 * мы внутри второго цикла for проверяем команды 
 * если команда заканчивается на access vlan
   * мы печатаем команду и добавляем к ней номер VLAN, обратившись в вложенному словарю по текущему ключу int
 * во всех остальных случаях, просто печатаем команду

В итоге мы получаем такой вывод:
```python
(test)nata@lab1:~$ python generate_access_port_config.py
interface FastEthernet0/12
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 11
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/16
 switchport mode access
 switchport access vlan 17
 spanning-tree portfast
 spanning-tree bpduguard enable
```
