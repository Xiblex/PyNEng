## generator (генератор)

Генераторы - это специальный класс функций, который позволяет легко создавать свои итераторы.
В отличии от обычных функций, генератор не просто возвращает значение и завершает работу, а возвращает итератор, который отдает элементы по одному.


Обычная функция завершает работу если:
* встретилось выражение return
* закончился код функции (это срабатывает как выражение ```return None```)
* возникло исключение

После выполнения функции, управление возвращается и программа выполняется дальше.
Все аргументы, которые передавались в функцию, локальные переменные, все это теряется.
Остается только результат, который вернула функция.

Функция может возвращать список элементов, несколько объектов или возвращать разные результаты, в зависимости от аргументов, но она всегда возвращает какой-то один результат.

Генератор же генерирует значения.
При этом, значения возвращаются по запросу и после возврата одного значения, выполнение функции-генератора приостанавливается до запроса следующего значения.
Между запросами генератор сохраняет свое состояние.


С точки зрения синтаксиса, генератор выглядит как обычная функция.
Но, вместо return, используется оператор ```yield```.

Каждый раз, когда внутри функции встречается yield, генератор приостанавливается и возвращает значение.
При следующем запросе, генератор начинает работать с того же места, где он завершил работу в прошлый раз.

Так как yield не завершает работу генератора, он может использоваться несколько раз.

Рассмотрим простой пример генератора:
```python
In [1]: def generate_nums(number):
   ...:     print('Start of generation')
   ...:     yield number
   ...:     print('Next number')
   ...:     yield number+1
   ...:     print('The end')
   ...:

```

Если вызвать генератор и присвоить результат в переменную, его код еще не будет выполняться:
```python
In [3]: result = generate_nums(100)
```

Теперь в переменной result находится итератор:
```python
In [4]: result
Out[4]: <generator object generate_nums at 0xb5788e9c>
```

Раз result это итератор, можно вызвать функцию next, чтобы получить значение:
```python
In [5]: next(result)
Start of generation
Out[5]: 100

```

После первого вызова next, генератор выполнил все строки до первого yield.
В данном случае, отобразилась строка 'Start of generation'.
Затем yield вернул значение - число 100.

Второй вызов next:
```python
In [6]: next(result)
Next number
Out[6]: 101
```

Выполнение продолжилось с предыдущего места - выведена строка 'Next number' и вернулось значение 101.

Следующий next:
```python
In [7]: next(result)
The end
------------------------------------------------------------
StopIteration              Traceback (most recent call last)
<ipython-input-7-1b214ba10814> in <module>()
----> 1 next(result)

StopIteration:

```

Так как в result находится итератор, когда элементы заканчиваются, он генерирует исключение StopIteration.
Но, до этого, вывелась строка 'The end'.

Раз функция-генератор возвращает итератор, его можно использовать в цикле:
```python
In [8]: for num in generate_nums(100):
   ...:     print('Number:', num)
   ...:
Start of generation
Number: 100
Next number
Number: 101
The end

```

С помощью генераторов зачастую можно написать ту же функцию с меньшим количеством промежуточных переменных.

Например, функцию такого вида:
```python
In [14]: def work_with_items(items):
    ...:     result = []
    ...:     for item in items:
    ...:         result.append('Changed {}'.format(item))
    ...:     return result
    ...:

In [15]: for i in work_with_items(range(10)):
    ...:     print(i)
    ...:
Changed 0
Changed 1
Changed 2
Changed 3
Changed 4
Changed 5
Changed 6
Changed 7
Changed 8
Changed 9
```

Можно заменить таким генератором:
```python
In [16]: def yield_items(items):
    ...:     for item in items:
    ...:         yield 'Changed {}'.format(item)
    ...:

In [17]: for i in yield_items(range(10)):
    ...:     print(i)
    ...:
Changed 0
Changed 1
Changed 2
Changed 3
Changed 4
Changed 5
Changed 6
Changed 7
Changed 8
Changed 9

```

При этом, генератор yield_items возвращает элементы по одному, а функция work_with_items - собирает их в список, а потом возвращает.
Если количество элементов небольшое, это не существенно.
Но, при обработке больших объемов данных, лучше работать с элементами по одному.

При этом, в любой момент, если действительно нужно получить все элементы, например, в виде списка, это можно сделать применив функцию list:
```python
In [20]: result =  yield_items(range(10))

In [21]: result
Out[21]: <generator object yield_items at 0xb579053c>

In [22]: list(result)
Out[22]:
['Changed 0',
 'Changed 1',
 'Changed 2',
 'Changed 3',
 'Changed 4',
 'Changed 5',
 'Changed 6',
 'Changed 7',
 'Changed 8',
 'Changed 9']
```

Например, при обработке большого log-файла, лучше обрабатывать его построчно, не выгружая все содержимое в память.

Допустим, нам нужно часто фильтровать определенные строки из файла.
Например, надо получить только строки, которые соответствуют регулярному выражению.
Конечно, можно каждый раз это делать в процессе обработки строк.
Но можно вынести подобную функциональность и в отдельную функцию.

Но только, в случае обычной функции, придется опять возвращать список или подобный объект.
А, если файл очень большой, то, скорее всего, придется отказаться от этой затеи.

Однако, если использовать генератор, файл будет обрабатываться построчно.
Это может быть, например, такой генератор:
```python
In [3]: import re

In [5]: def filter_lines(filename, regex):
   ...:     with open(filename) as f:
   ...:         for line in f:
   ...:             if re.search(regex, line):
   ...:                 yield line.rstrip()
   ...:

```

Генератор проходится по указанному файлу и отдает те строки, которые совпали с регулярным выражением.

Пример использования:
```python
In [7]: for line in filter_lines('config_r1.txt', '^interface'):
   ...:     print(line)
   ...:
interface Loopback0
interface Tunnel0
interface Ethernet0/0
interface Ethernet0/1
interface Ethernet0/2
interface Ethernet0/3
interface Ethernet0/3.100
interface Ethernet1/0

```

Но генераторы могут использоваться не только в том случае, когда надо возвращать элементы по одному.

Например, генератор get_cdp_neighbor читает файл с выводом sh cdp neighbor detail и выдает вывод частями, по одному соседу:
```python
def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        line = ''
        while True:
            while not 'Device ID' in line:
                line = f.readline()
            neighbor = ''
            neighbor += line
            for line in f:
                if line.startswith('-----'):
                    break
                neighbor += line
            yield neighbor
            line = f.readline()
            if not line:
                return

```

Полный скрипт выглядит таким образом (файл parse_cdp_file.py):
```python
import re
from pprint import pprint

def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        line = ''
        while True:
            while not 'Device ID' in line:
                line = f.readline()
            neighbor = ''
            neighbor += line
            for line in f:
                if line.startswith('-----'):
                    break
                neighbor += line
            yield neighbor
            line = f.readline()
            if not line:
                return


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

Так как генератор get_cdp_neighbor выдает каждый раз вывод про одного соседа, можно проходиться по результату в цикле и передавать каждый вывод функции parse_cdp (из подраздела [re.finditer раздела по регулярным выражениям](https://natenka.gitbooks.io/pyneng/content/v/python3.6/book/09_regex/5_re_finditer.html)).

И конечно же, полученный результат тоже можно не собирать в один большой словарь, а передавать куда-то дальше на обработку или запись.

Результат выполнения:
```
$ python parse_cdp_file.py
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

В следующем подразделе мы значительно сократим код в функции get_cdp_neighbor, использовав функции из itertools.

