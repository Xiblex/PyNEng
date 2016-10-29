## Модуль multiprocessing

Модуль multiprocessing предлагает интерфейс подобный модулю threading, но при этом, мы уже используем не потоки, а процессы.

Каждому процессу выделяются свои ресурсы. Кроме того, у каждого процесса свой GIL, а значит, у нас нет тех проблем, которые были с потоками и код может выполняться параллельно и задействовать ядра/процессоры компьютера.

Пример использования модуля multiprocessing:
```python
import multiprocessing
from netmiko import ConnectHandler
import sys
import yaml


COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command, queue):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)

    print "Connection to device %s" % device_dict['ip']
    queue.put({device_dict['ip']: result})


def conn_processes(function, devices, command):
    processes = []
    queue = multiprocessing.Queue()

    for device in devices:
        p = multiprocessing.Process(target = function, args = (device, command, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = []
    for p in processes:
        results.append(queue.get())

    return results

print( conn_processes(connect_ssh, devices['routers'], COMMAND) )
```

Обратите внимание, что этот пример аналогичен последнему примеру, который мы использовали с модулем threading. Единственное отличие в том, что с multiprocessing нам не надо использовать модуль Queue, так как у модуля multiprocessing есть своя реализация очереди.

Если проверить время исполнения этого скрипта, аналогичного для модуля threading и последовательного подключения, то получаем такую картину:
```
последовательное: 5.833s
threading:        2.225s
multiprocessing:  2.365s
```

Время выполнения для модуля multiprocessing немного больше, но это связано с тем, что на создание процессов уходит больше времени, чем на создание потоков. И, если бы скрипт был сложнее и выполнялось больше задач, или было бы больше подключений, тогда бы multiprocessing начал бы существенно выигрывать у модуля threading.


