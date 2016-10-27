# -*- coding: utf-8 -*-
'''
Задание 12.4

В задании используется пример из раздела про [модуль threading](book/chapter12/5a_threading.md).

Переделать пример таким образом, чтобы:
* функция connect_ssh не выводила результат выполнения команды на стандартный поток вывода, а возвращала вывод.
* пример надо изменить так, чтобы в результате выполнение команды на всех устройствах, возвращался словарь, где:
 * ключ - IP-адрес устройства
 * значение - результат вывода команды

'''

from netmiko import ConnectHandler
import sys
import yaml
import threading

COMMAND = sys.argv[1]
all_devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)

    print "Connection to device %s" % device_dict['ip']
    print result


def conn_threads(function, devices, command):
    threads = []
    for device in devices:
        th = threading.Thread(target = function, args = (device, command))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

conn_threads(connect_ssh, all_devices['routers'], COMMAND)
