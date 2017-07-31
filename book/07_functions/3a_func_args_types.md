## Типы аргументов функции

При вызове функции аргументы можно передавать двумя способами:
* как __позиционные__ - передаются в том же порядке, в котором они определены, при создании функции. То есть, порядок передачи аргументов, определяет какое значение получит каждый
* как __ключевые__ - передаются с указанием имени аргумента и его значения. В таком случае, аргументы могут быть указаны в любом порядке, так как их имя указывается явно.

Позиционные и ключевые аргументы могут быть смешаны, при вызове функции.
То есть, можно использовать оба способа, при передаче аргументов одной и той же функции.
При этом, сначала должны идти позиционные аргументы, а только потом - ключевые.

> Код функций, которые используются в этом разделе, можно скопировать из файла func_args_types.py

Посмотрим на разные способы передачи аргументов, на примере функции:
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
  ....:
```

### Позиционные аргументы

Позиционные аргументы, при вызове функции, надо передать в правильном порядке (поэтому они и называются позиционные)

```python
In [2]: cfg_to_list('r1.txt', False)
Out[2]:
['!',
 'service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 '!',
 'no ip domain lookup',
 '!',
 '',
 '',
 'ip ssh version 2',
 '!']
```

Если при вызове функции поменять аргументы местами, скорее всего, возникнет ошибка, в зависимости от конкретной функции.


### Ключевые аргументы
__Ключевые аргументы__:
* передаются с указанием имени аргумента
* за счет этого, они могут передаваться в любом порядке

Если передать оба аргумента, как ключевые, можно передавать их в любом порядке:
```python
In [4]: cfg_to_list(delete_exclamation=False, cfg_file='r1.txt')
Out[4]:
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

__Но, обратите внимание, что всегда сначала должны идти позиционные аргументы, а затем ключевые.__

Если сделать наоборот, возникнет ошибка:
```python
In [5]: cfg_to_list(delete_exclamation=False, 'r1.txt')
  File "<ipython-input-3-8f3a3aa16a22>", line 1
    cfg_to_list(delete_exclamation=False, 'r1.txt')
                                         ^
SyntaxError: positional argument follows keyword argument

```

Но в такой комбинации можно:
```python
In [6]: cfg_to_list('r1.txt', delete_exclamation=True)
Out[6]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']

```

> В реальной жизни, зачастую намного понятней и удобней указывать флаги, такие как delete_exclamation, как ключевой аргумент. Если задать хорошее название параметра, за счет указания его имени, сразу будет понятно, что именно делает этот аргумент.

> Например, в функции cfg_to_list, понятно, что аргумент delete_exclamation приводит к удалению восклицательных знаков.
