### Пример использования ключевых аргументов переменной длинны и распаковки аргументов

Посмотрим, как с помощью аргументов переменной длинны можно передавать аргументы между функциями.


Допустим, у нас есть функция config_to_list (файл kwargs_example.py):
```python
def config_to_list(cfg_file, delete_excl=True,
                   delete_empty=True, strip_end=True):
    result = []
    with open( cfg_file ) as f:
        for line in f:
            if strip_end:
                line = line.rstrip()
            if delete_empty and not line:
                pass
            elif delete_excl and line.startswith('!'):
                pass
            else:
                result.append(line)
    return result
```

> Весь код функции можно вставить в ipython с помощью команды ```%cpaste```.

Она берет файл с конфигурацией, убирает часть строк и возвращает остальные строки как список.

Попробуем вызывать её в ipython:
```python
In [1]: config_to_list('r1.txt')
Out[1]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

По умолчанию, из конфигурации убираются пустые строки, перевод строки в конце строк и строки, которые начинаются на знак восклицания.

Попробуем поменять какой-то параметр по умолчанию:
```python
In [2]: config_to_list('r1.txt', delete_empty=False)
Out[2]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 '',
 '',
 'ip ssh version 2']

```

Теперь пустые строки появились в списке.

Теперь мы хотим сделать 'оберточную' функцию clear_cfg_and_write_to_file, которая берет файл конфигурации, с помощью функции config_to_list, удаляет лишние строки и затем записывает строки в указанный файл.

Но, при этом, мы не хотим терять возможность управлять тем, какие строки будут отброшены.
То есть, мы хотим, чтобы функция clear_cfg_and_write_to_file поддерживала те же параметры, что и функция config_to_list.

Мы можем сделать её такой:
```python
def clear_cfg_and_write_to_file(cfg, to_file, delete_excl=True,
                                delete_empty=True, strip_end=True):

    cfg_as_list = config_to_list(cfg, delete_excl=delete_excl,
                    delete_empty=delete_empty, strip_end=strip_end)
    with open(to_file, 'w') as f:
        f.write('\n'.join(cfg_as_list))
```

То есть, нам пришлось повторить все параметры.
И потом передавать все их в функцию config_to_list.


Но, если мы воспользуемся возможностю Python принимать аргументы переменной длины, мы можем сделать функцию clear_cfg_and_write_to_file такой:
```python
def clear_cfg_and_write_to_file(cfg, to_file, **kwargs):
    cfg_as_list = config_to_list(cfg, **kwargs)
    with open(to_file, 'w') as f:
        f.write('\n'.join(cfg_as_list))
```

То есть, в функции clear_cfg_and_write_to_file мы явно прописали её аргументы, а всё остальное попадет в переменную kwargs.
А затем мы её передаем в функцию config_to_list.

> В этом примере, ```**kwargs``` используется и для того, чтобы указать, что функция clear_cfg_and_write_to_file может принимать аргументы переменной длинны, и для того, чтобы 'распаковать' словарь kwargs, когда мы передаем его в функцию config_to_list.

Так функция clear_cfg_and_write_to_file выглядит проще и понятней.
И мы можем спокойно добавлять аргументы в функцию config_to_list, без необходимости дублировать их в функции clear_cfg_and_write_to_file.

