## Модуль itertools

В Python есть отдельный модуль itertools в котором находятся итераторы и средства работы с ними.

Например, в этом модуле есть бесконечные итераторы:
* count() - этот итератор возвращает номера, начиная с указанного и используя указанный шаг
* cycle() - повторяет циклически элементы
* repeat() - повторяет элемент


### count

Пример count():
```python
In [21]: import itertools

In [22]: count_nums = itertools.count(0,2)

In [23]: count_nums
Out[23]: count(0, 2)

In [24]: for _ in range(10):
    ...:     print(next(count_nums))
    ...:
0
2
4
6
8
10
12
14
16
18

```

Например, count может пригодиться в zip, чтобы сгенерировать номера элементов:
```python
In [25]: nums = list(range(100, 201, 10))

In [26]: nums
Out[26]: [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

In [27]: list(zip(itertools.count(), nums))
Out[27]:
[(0, 100),
 (1, 110),
 (2, 120),
 (3, 130),
 (4, 140),
 (5, 150),
 (6, 160),
 (7, 170),
 (8, 180),
 (9, 190),
 (10, 200)]
```

### cycle

Пример использования cycle():
```python
In [28]: cycle_letters = itertools.cycle('ABCD')

In [29]: for _ in range(10):
    ...:     print(next(cycle_letters))
    ...:
A
B
C
D
A
B
C
D
A
B

```

### islice

Функция islice создает итератор, который возвращает элементы итерируемого объекта.
Она поддерживает такой же синтаксис, как и функция range:
```python
In [30]: from itertools import islice

In [31]: islice(range(100,200,5), 5)
Out[31]: <itertools.islice at 0xb4f6c57c>

In [32]: list(islice(range(100,200,5), 5))
Out[32]: [100, 105, 110, 115, 120]

In [33]: list(islice(range(100,200,5), 5, 10))
Out[33]: [125, 130, 135, 140, 145]

In [34]: list(islice(range(100,200,5), 5, 10, 2))
Out[34]: [125, 135, 145]

```

> islice не поддерживает отрицательные индексы


С помощью функций, которые находятся в модуле itertools, можно создавать полезные функции для работы с итерируемыми объектами или итератораторами.

Пример из документации модуля:
```python
In [35]: from itertools import islice

In [36]: def take(n, iterable):
    ...:     "Return first n items of the iterable as a list"
    ...:     return list(islice(iterable, n))
    ...:
```

Функция take возвращает указанное количество элементов из итерируемого объекта:
```python
In [37]: a = [1,2,3,4,5,6,7,8]

In [38]: b = range(100,200,5)

In [39]: take(5, a)
Out[39]: [1, 2, 3, 4, 5]

In [40]: take(5, b)
Out[40]: [100, 105, 110, 115, 120]

```

### dropwhile

Функция dropwhile ожидает как аргументы функцию, которая возвращает True или False, в зависимости от условия, и итерируемый объект.
Функция dropwhile отбрасывает элементы итерируемого объекта до тех пор, пока функция переданная как аргумент возвращает True.
Как только dropwhile встречает False, он возвращает итератор с оставшимися объектами.

Пример:
```python
In [1]: from itertools import dropwhile

In [2]: list(dropwhile(lambda x: x < 5, [0,2,3,5,10,2,3]))
Out[2]: [5, 10, 2, 3]

```

В данном случае, как только функция dropwhile дошла до числа, которое больше или равно пяти, она вернула все оставшиеся числа.
При этом, даже если далее есть числа, которые меньше 5, функция уже не проверяет их.

### takewhile

Функция takewhile є абсолютная противоположность функции dropwhile: она возвращает итератор с теми элементами, которые соответствуют условию, до первого ложного условия:
```python
In [3]: from itertools import takewhile

In [4]: list(takewhile(lambda x: x < 5, [0,2,3,5,10,2,3]))
Out[4]: [0, 2, 3]

```


### Пример использования takewhile и dropwhile

В прошлом разделе был создан генератор get_cdp_neighbor, который возвращает вывод sh cdp neighbors detail по одному соседу.

Логика функции была такая:
* сначала надо отбросить все, пока не встретится строка с Device ID
* затем надо взять все строки, пока  не встретится строка с '-----'
* потом начать все с начала

В прошлом варианте эта функциональность реализована циклами.
Но первое условие - это именно то, что делает функция dropwhile, а второе - то, что делает функция takewhile.

В итоге, генератор выглядит так:
```python
def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        while True:
            begin = dropwhile(lambda x: not 'Device ID' in x, f)
            lines = takewhile(lambda y: not '-----' in y, begin)
            neighbor = ''.join(lines)
            if not neighbor:
                return
            yield neighbor
```

Остальные части скрипта никак не поменялись (файл parse_cdp_file_ver2.py):
```python
import re
from pprint import pprint
from itertools import dropwhile, takewhile

def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        while True:
            f = dropwhile(lambda x: not 'Device ID' in x, f)
            lines = takewhile(lambda y: not '-----' in y, f)
            neighbor = ''.join(lines)
            if not neighbor:
                return
            yield neighbor


def parse_cdp(output):
    regex = ('Device ID: (?P<device>\S+)'
             '|IP address: (?P<ip>\S+)'
             '|Platform: (?P<platform>\S+ \S+),'
             '|Cisco IOS Software, (?P<ios>.+), RELEASE')

    result = {}

    match_iter = re.finditer(regex, output)
    for match in match_iter:
        if match.lastgroup == 'device':
            device = match.group(match.lastgroup)
            result[device] = {}
        elif device:
            result[device][match.lastgroup] = match.group(match.lastgroup)

    return result


filename = 'sh_cdp_neighbors_detail.txt'
result = get_cdp_neighbor(filename)

all_cdp = {}
for cdp in result:
    all_cdp.update(parse_cdp(cdp))

pprint(all_cdp)

```


Результат аналогичный:
```
$ python parse_cdp_file_ver2.py
{'R1': {'ios': '3800 Software (C3825-ADVENTERPRISEK9-M), Version 12.4(24)T1',
        'ip': '10.1.1.1',
        'platform': 'Cisco 3825'},
 'R2': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.2.2.2',
        'platform': 'Cisco 2911'},
 'R3': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.3.3.3',
        'platform': 'Cisco 2911'},
 'SW2': {'ios': 'C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9',
         'ip': '10.1.1.2',
         'platform': 'cisco WS-C2960-8TC-L'}}
```

