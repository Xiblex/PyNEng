# Упражнения

###Задание 3.1

Обработать строку ospf_route и вывести информацию в виде:
```
Protocol:				OSPF
Prefix:					10.0.24.0/24
AD/Metric:				110/41
Next-Hop:				10.0.13.3
Last update:			3d18h
Outbound Interface:		FastEthernet0/0
```

```python
ospf_route = "O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
```

###Задание 3.2
Список mac содержит MAC-адреса в формате XXXX:XXXX:XXXX.

Однако, в оборудовании Cisco MAC-адреса используются в формате XXXX.XXXX.XXXX.

Создать скрипт, который преобразует MAC-адреса в формат cisco и добавляет их в новый список mac_cisco.

Усложненный вариант: сделать преобразование в одну строку.
