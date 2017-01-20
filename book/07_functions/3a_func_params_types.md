## Типы параметров функции

При создании функции, мы можем определять, какие аргументы нужно передавать обязательно, а какие нет.

Соответственно, функция может быть создана с параметрами:
* __обязательными__
* __необязательными__ (опциональными, аргументами со значением по умолчанию)

### Обязательные параметры

__Обязательные параметры__: определяют какие аргументы нужно передать функции обязательно. При этом, их нужно передать ровно сколько, сколько указано параметров функции (нельзя указать большее или меньшее количество аргументов)

Функция с обязательными параметрами:
```python
In [1]: def cfg_to_list(cfg_file, delete_exclamation):
  ....:     result = []
  ....:     with open( cfg_file ) as f:
  ....:         for line in f:
  ....:             if delete_exclamation and line.startswith('!'):
  ....:                 pass
  ....:             else:
  ....:                 result.append(line.rstrip())
  ....:     return result
```

Функция cfg_to_list ожидает два аргумента: cfg_file и delete_exclamation.

Внутри, она открывает файл cfg_file для чтения, проходится по всем строкам и,
если аргумент delete_exclamation истина и строка начинается с восклицательного знака,
строка пропускается.
Оператор ```pass``` означает, что ничего не выполняется.

Во всех остальных случаях, в строке справа удаляются символы перевода строки и строка добавляется в словарь result.

Попробуем вызвать функцию, указав аргументы, как позиционные:
```python
In [2]: cfg_to_list('r1.txt', True)
Out[2]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

Так как мы передали значение True аргументу delete_exclamation, строк с восклицательными знаками нет в итоговом словаре.

Теперь попробуем вызвать функцию ещё раз, передав аргументу delete_exclamation значение False:
```python
In [3]: cfg_to_list('r1.txt', False)
Out[3]:
['!',
 'service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 '!',
 'no ip domain lookup',
 '!',
 'ip ssh version 2',
 '!']
```

### Необязательные параметры (параметры со значением по умолчанию)

При создании функции, можно указывать значение по умолчанию для параметра:
```python
In [4]: def cfg_to_list(cfg_file, delete_exclamation=True):
  ....:     result = []
  ....:     with open( cfg_file ) as f:
  ....:         for line in f:
  ....:             if delete_exclamation and line.startswith('!'):
  ....:                 pass
  ....:             else:
  ....:                 result.append(line.rstrip())
  ....:     return result
  ....:

```

Так как теперь у параметра delete_exclamation значение по умолчанию равно True,
соответствующий аргумент можно не указывать при вызове функции, если нам подходит значение по умолчанию:
```python
In [5]: cfg_to_list('r1.txt')
Out[5]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

Но, можно и указать, если нужно поменять значение по умолчанию:
```python
In [6]: cfg_to_list('r1.txt', False)
Out[6]:
['!',
 'service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 '!',
 'no ip domain lookup',
 '!',
 'ip ssh version 2',
 '!']

```

