# -*- coding: utf-8 -*-
'''
Задание 14.1

Переделать пример, который использовался в разделе TextFSM, в функцию.

Функция должна называться parse_output:
* аргументы функции:
 * template - шаблон TextFSM (это должно быть имя файла, в котором находится шаблон)
 * output - вывод соответствующей команды show (строка)

Функция должна возвращать два списка:
* список с названиями столбцов (в примере ниже, находится в переменной header)
* список списков, в котором находятся результаты обработки вывода (в примере ниже, находится в переменной result)

Проверить работу функции.

Пример из раздела:
'''

import sys
import textfsm
from tabulate import tabulate

template = sys.argv[1]
output_file = sys.argv[2]

f = open(template)
output = open(output_file).read()

re_table = textfsm.TextFSM(f)

header = re_table.header
result = re_table.ParseText(output)

print tabulate(result, headers=header)
