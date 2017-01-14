## Строки (Strings)
Строки это неизменяемый, упорядоченный тип данных.

Строка в Python это последовательность символов, заключенная в кавычки.

Примеры строк:
```python
In [9]: 'Hello'
Out[9]: 'Hello'
In [10]: "Hello"
Out[10]: 'Hello'

In [11]: tunnel = __
   ....: interface Tunnel0
   ....:  ip address 10.10.10.1 255.255.255.0
   ....:  ip mtu 1416
   ....:  ip ospf hello-interval 5
   ....:  tunnel source FastEthernet1/0
   ....:  tunnel protection ipsec profile DMVPN
   ....: __

In [12]: tunnel
Out[12]: '\ninterface Tunnel0\n ip address 10.10.10.1 255.255.255.0\n ip mtu 1416\n ip ospf hello-interval 5\n tunnel source FastEthernet1/0\n tunnel protection ipsec profile DMVPN\n'

In [13]: print tunnel

interface Tunnel0
 ip address 10.10.10.1 255.255.255.0
 ip mtu 1416
 ip ospf hello-interval 5
 tunnel source FastEthernet1/0
 tunnel protection ipsec profile DMVPN
```

То, что строки являются упорядоченным типом данных позволяет нам обращаться к символам в строке по номеру, начиная с нуля:
```python
In [14]: string1 = 'interface FastEthernet1/0'

In [15]: string1[0]
Out[15]: 'i'
```

Нумерация всех символов в строке идет с нуля. Но, если нужно обратиться к какому-то по счету символу, начиная с конца, то можно указывать отрицательные значения (на этот раз с единицы).

```python
In [16]: string1[1]
Out[16]: 'n'

In [17]: string1[-1]
Out[17]: '0'
```

Кроме обращения к конкретному символу, можно делать срезы строки, указав диапазон номеров (срез выполняется по второе число, не включая его):
```python
In [18]: string1[0:9]
Out[18]: 'interface'

In [19]: string1[10:22]
Out[19]: 'FastEthernet'
```

Если не указывается второе число, то срез будет до конца строки:
```python
In [20]:  string1[10:]
Out[20]: 'FastEthernet1/0'
```

Срезать три последних символа строки:
```python
In [21]: string1[-3:]
Out[21]: '1/0'
```

Строка в обратном порядке:
```python
In [22]: a = '0123456789'

In [23]: a[::]
Out[23]: '0123456789'

In [24]: a[::-1]
Out[24]: '9876543210'
```
