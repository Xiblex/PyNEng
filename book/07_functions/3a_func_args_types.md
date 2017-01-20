## Типы аргументов

При создании функции, мы можем определять, какие аргументы нужно передавать обязательно, а какие нет.

Соответственно, функция может быть создана с аргументами:
* __обязательными__
* __необязательными__ (опциональными, аргументами со значением по умолчанию)

### Обязательные аргументы

__Обязательные аргументы__: надо передать ровно сколько, сколько указано параметров функции (нельзя указать большее или меньшее количество аргументов)

Функция с обязательными аргументами:
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

### Необязательные аргументы (аргументы со значением по умолчанию)

При создании функции, можно указывать значение по умолчанию для аргумента:
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

Так как теперь у аргумента delete_exclamation значение по умолчанию равно True,
этот аргумент можно не указывать при вызове функции, если нам подходит значение по умолчанию:
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

## Передача аргументов, при вызове функции

Когда мы вызываем функцию, мы можем передавать аргументы двумя способами:
* как __позиционные__ - мы передаем аргументы в том же порядке, в котором они определены, при создании функции. То есть, порядок передачи аргументов, определяет какое значение получит каждый
* как __ключевые__ - мы передаем аргументы, указывая имя аргумента и значение. В таком случае, аргументы могут быть указаны в любом порядке, так как мы явно указываем их имя.

Позицонные и ключевые аргументы могут быть смешаны, при вызове функции.
То есть, можно использовать и тот и тот способ, при передаче аргументов одной и той же функции.

Но, при этом, сначала должны идти позиционные аргументы, а только потом - ключевые.

Посмотрим на разные способы передачи аргументов, на примере функции:
```python
In [7]: def cfg_to_list(cfg_file, delete_exclamation):
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

### Позиционные аргументы

Позиционные аргументы, при вызове функции, надо передать в правильном порядке (поэтому они и называются позиционные)


Если мы, при вызове поменяем аргументы местами, скорее всего, возникнет ошибка, в зависимости о конкретной функции.

В нашем случае, получается такой результат:
```python
In [8]: cfg_to_list(False, 'r1.txt')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-18-e6da7e2657eb> in <module>()
----> 1 cfg_to_list(False, 'r1.txt')

<ipython-input-15-21a013e5e92c> in cfg_to_list(cfg_file, delete_exclamation)
      1 def cfg_to_list(cfg_file, delete_exclamation):
      2     result = []
----> 3     with open( cfg_file ) as f:
      4         for line in f:
      5             if delete_exclamation and line.startswith('!'):

TypeError: coercing to Unicode: need string or buffer, bool found
```

### Ключевые аргументы
__Ключевые аргументы__:
* передаются с указанием именем аргумента
* засчет этого, они могут передаваться в любом порядке

Если мы теперь передадим оба аргумента, как ключевые, то мы можем передавать их в любом порядке:
```python
In [9]: cfg_to_list(delete_exclamation=False, cfg_file='r1.txt')
Out[9]:
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

__Но, обратите внимание, что всегда сначала должны идти обязательные (позиционные) аргументы, а затем ключевые.__

Если мы сделаем наоборот, возникнет ошибка:
```python
In [10]: cfg_to_list(delete_exclamation=False, 'r1.txt')
  File "<ipython-input-19-5efdee7ce6dd>", line 1
    cfg_to_list(delete_exclamation=False, 'r1.txt')
SyntaxError: non-keyword arg after keyword arg

```

Но в такой комбинации можно:
```python
In [11]: cfg_to_list('r1.txt', delete_exclamation=True)
Out[11]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']

```

> В реальной жизни, зачастую намного понятней и удобней указывать флаги, такие как delete_exclamation, как ключевой аргумент. Если вы использовали хорошее название параметра, засчет указания его имени, сразу будет понятно, что именно делает этот аргумент.

> Например, в нашем случае, понятно, что этот аргумент удаляет восклицательные знаки.
