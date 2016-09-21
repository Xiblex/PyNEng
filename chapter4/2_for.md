## for
Цикл for проходится по указанной последовательности и выполняет действия, которые указаны в блоке for. 

Примеры последовательностей, по которым может проходиться цикл for:
* строка
* список
* словарь
* функция range() или итератор xrange()
* любой другой итератор (например, sorted(), enumerate())

Цикл for проходится по строке:
```python
In [1]: for letter in 'Test string':
   ...:     print letter
   ...:     
T
e
s
t
 
s
t
r
i
n
g
```

В цикле мы использовали переменную с именем __letter__. Хотя имя может быть любое, удобно, когда имя подсказывает через какие объекты проходит цикл.

Пример цикла for с функцией range():
```python
In [2]: for i in xrange(10):
   ...:     print 'interface FastEthernet0/' + str(i)
   ...:     
interface FastEthernet0/0
interface FastEthernet0/1
interface FastEthernet0/2
interface FastEthernet0/3
interface FastEthernet0/4
interface FastEthernet0/5
interface FastEthernet0/6
interface FastEthernet0/7
interface FastEthernet0/8
interface FastEthernet0/9
```

В этом цикле мы использовали итератор xrange(). Этот итератор генерирует числа в диапазоне от нуля, до указанного числа, не включая его.


> В Python есть функция range() и итератор xrange().

> В реальной жизни лучше использовать xrange(), так как в этом случае генерируется не весь список чисел сразу, как в range(), а значения выдаются циклу по мере обращения.



В этом примере, мы проходим по списку VLAN, поэтому переменную можно назвать vlan:
```python
In [3]: vlans = [10, 20, 30, 40, 100]
In [4]: for vlan in vlans:
   ...:     print 'vlan %d' % vlan
   ...:     print ' name VLAN_%d' % vlan
   ...:     
vlan 10
 name VLAN_10
vlan 20
 name VLAN_20
vlan 30
 name VLAN_30
vlan 40
 name VLAN_40
vlan 100
 name VLAN_100
```

Когда цикл идет по словарю, то фактически он проходится по ключам:
```python
In [5]: r1 = {
 'IOS': '15.4',
 'IP': '10.255.0.1',
 'hostname': 'london_r1',
 'location': '21 New Globe Walk',
 'model': '4451',
 'vendor': 'Cisco'}

In [12]: for k in r1:
   ....:     print k
   ....:     
vendor
IP
hostname
IOS
location
model
```

Если необходимо выводить пары ключ-значение в цикле:
```python
In [6]: for key in r1:
   ....:     print key + ' => ' + r1[key]
   ....:     
vendor => Cisco
IP => 10.255.0.1
hostname => london_r1
IOS => 15.4
location => 21 New Globe Walk
model => 4451
```

Или так:
```python
In [6]: for key, value in r1.items():
   ....:     print key + ' => ' + value
   ....:     
vendor => Cisco
IP => 10.255.0.1
hostname => london_r1
IOS => 15.4
location => 21 New Globe Walk
model => 4451
```

