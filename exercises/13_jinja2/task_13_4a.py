# -*- coding: utf-8 -*-

"""
Задание 13.4a

Создайте функцию add_vlan, которая использует:
* шаблон templates/add_vlan_to_switch.txt
* функцию generate_cfg_from_template

Функция add_vlan должна возвращать список команд,
на основе шаблона templates/add_vlan_to_switch.txt

Параметры функции:
- ip коммутатора
- vlan: name
- access: intf
- trunk: intf

Возвращает список команд


Проверьте шаблон templates/add_vlan_to_switch.txt
на данных в файле data_files/add_vlan_to_switch.yaml,
с помощью функции generate_cfg_from_template из задания 13.1-13.1d.
Не копируйте код функции.

"""

