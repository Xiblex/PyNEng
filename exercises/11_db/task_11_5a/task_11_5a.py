# -*- coding: utf-8 -*-

"""
Задание 11.5a

После выполнения задания 11.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data.py, таким образом, чтобы он удалял все записи,
которые были активными более недели назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active.

В файле задания описан пример работы с объектами модуля datetime.
Обратите внимание, что объекты, как и строки с датой, которые мы пишем в БД,
можно сравнивать между собой.
"""

from datetime import timedelta, datetime

now = datetime.today().replace(microsecond=0)
two_weeks_ago = now - timedelta(days = 14)

#print now
#print seven_days_ago
#print now > seven_days_ago
#print now.__str__() > seven_days_ago.__str__()

# now_string нужна для того, чтобы записать время записи в БД в виде строки
now_string = now.__str__()
