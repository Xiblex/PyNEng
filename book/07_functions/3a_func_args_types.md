## Типы аргументов функции

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

__Но, обратите внимание, что всегда сначала должны идти позиционные аргументы, а затем ключевые.__

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
