# -*- coding: utf-8 -*-

'''
Это копия примера из раздела
'''

import sqlite3
import sys

db_filename = 'dhcp_snooping.db'


key, value = sys.argv[1:]
keys = ['mac', 'ip', 'vlan', 'interface']
keys.remove(key)

with sqlite3.connect(db_filename) as conn:
    #Позволяет далее обращаться к данным в колонках, по имени колонки
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("select * from dhcp where %s = ?" % key, (value,))

    print "\nDetailed information for host(s) with", key, value
    print '-' * 40
    for row in cursor.fetchall():
        for k in keys:
            print "%-12s: %s" % (k, row[k])
        print '-' * 40
