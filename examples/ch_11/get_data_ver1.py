# -*- coding: utf-8 -*-
import sqlite3
import sys

db_filename = 'dhcp_snooping.db'

if len(sys.argv) == 1:
    print "\nВ таблице dhcp такие записи:"
    print '-' * 70
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute('select * from dhcp')

        for row in cursor.fetchall():
            print '%-18s %-17s %-5s %-20s' % row

elif len(sys.argv) == 3:
    key, value = sys.argv[1:]
    keys = ['mac', 'ip', 'vlan', 'interface']
    #Проверка указанного ключа (параметра)
    if key in keys:
        keys.remove(key)
        with sqlite3.connect(db_filename) as conn:
            #Позволяет далее обращаться к данным в колонках, по имени колонки
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()

            cursor.execute("select * from dhcp where %s = ?" % key, (value,))

            print "\nDetailed information for host(s) with", key, value
            print '-' * 40
            for row in cursor.fetchmany(10):
                for k in keys:
                    print "%-12s: %s" % (k,row[k])
                print '-' * 40
    else:
        print "Данный параметр не поддерживается."
        print "Допустимые значения параметров: mac, ip, vlan, interface"
else:
    print "Введите, пожалуйста, два параметра"


"""
Example:

$ python get_data_ver1.py

В таблице dhcp такие записи:
----------------------------------------------------------------------
00:09:BB:3D:D6:58  10.1.10.2         10    FastEthernet0/1
00:04:A3:3E:5B:69  10.1.5.2          5     FastEthernet0/10
00:05:B3:7E:9B:60  10.1.5.4          5     FastEthernet0/9
00:07:BC:3F:A6:50  10.1.10.6         10    FastEthernet0/3
00:09:BC:3F:A6:50  192.168.100.100   1     FastEthernet0/7


$ python get_data_ver1.py ip 10.1.10.2

Detailed information for host(s) with ip 10.1.10.2
----------------------------------------
mac         : 00:09:BB:3D:D6:58
vlan        : 10
interface   : FastEthernet0/1
----------------------------------------


$ python get_data_ver1.py vlan 10

Detailed information for host(s) with vlan 10
----------------------------------------
mac         : 00:09:BB:3D:D6:58
ip          : 10.1.10.2
interface   : FastEthernet0/1
----------------------------------------
mac         : 00:07:BC:3F:A6:50
ip          : 10.1.10.6
interface   : FastEthernet0/3
----------------------------------------


$ python get_data_ver1.py vln 10
Данный параметр не поддерживается.
Допустимые значения параметров: mac, ip, vlan, interface


$ python get_data_ver1.py vlan
Введите, пожалуйста, два параметра
"""
