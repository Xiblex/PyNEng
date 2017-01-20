## Аргументы переменной длинны

Иногда заведомо неизвестно сколько аргументов надо передавать функции. Для таких ситуаций мы можем создавать функцию с параметрами переменной длинны.

Такой параметр может быть, как ключевым, так и позиционным.


> Чаще всего, аргументы переменной длины используются в более сложных конструкциях Python. То есть, скорее всего, они вам не скоро понадобятся.

> Но, даже если вам не нужно будет их использовать, есть большая вероятность, что, когда вы будете разбираться чужом коде, вы натолкнетесь на них.

### Позиционные аргументы переменной длинны
Начнем с позиционного:
```python
In [1]: def sum_arg(a,*arg):
   ....:     print a, arg
   ....:     return a + sum(arg)
   ....: 
```

Функция sum_arg создана с двумя параметрами:
* параметр a
 * если передается как позиционный аргумент, должен идти первым
 * если передается как ключевой аргумент, то порядок не важен
* параметр *arg - ожидает аргументы переменной длины
 * сюда попадут все остальные аргументы в виде кортежа
 * эти аргументы могут отсутствовать

Попробуем вызвать функцию:
```python
In [2]: sum_arg(1,10,20,30)
1 (10, 20, 30)
Out[2]: 61

In [3]: sum_arg(1,10)
1 (10,)
Out[3]: 11

In [4]: sum_arg(1)
1 ()
Out[4]: 1
```

А можно было создать такую функцию:
```python
In [5]: def sum_arg(*arg):
   ....:     print arg
   ....:     return sum(arg)
   ....: 

In [6]: sum_arg(1,10,20,30)
(1, 10, 20, 30)
Out[6]: 61

In [7]: sum_arg()
()
Out[7]: 0
```

### Ключевые аргументы переменной длинны
Аналогичным образом можно создать параметр переменной длины для ключевых аргументов:
```python
In [8]: def sum_arg(a,**karg):
   ....:     print a, karg
   ....:     return a + sum(karg.values())
   ....: 
```

Функция sum_arg создана с двумя параметрами:
* параметр a
 * если передается как позиционный аргумент, должен идти первым
 * если передается как ключевой аргумент, то порядок не важен
* параметр **karg - ожидает ключевые аргументы переменной длины
 * сюда попадут все остальные ключевые аргументы в виде словаря
 * эти аргументы могут отсутствовать

Попробуем вызвать функцию:
```python
In [9]: sum_arg(a=10,b=10,c=20,d=30)
10 {'c': 20, 'b': 10, 'd': 30}
Out[9]: 70

In [10]: sum_arg(b=10,c=20,d=30,a=10)
10 {'c': 20, 'b': 10, 'd': 30}
Out[10]: 70
```

Обратите внимание, что, хотя a можно указывать как позиционный аргумент, нельзя указывать позиционный аргумент после ключевого:
```python
In [11]: sum_arg(10,b=10,c=20,d=30)
10 {'c': 20, 'b': 10, 'd': 30}
Out[11]: 70

In [12]: sum_arg(b=10,c=20,d=30,10)
  File "<ipython-input-6-71c121dc2cf7>", line 1
    sum_arg(b=10,c=20,d=30,10)
SyntaxError: non-keyword arg after keyword arg
```

### Пример использования ключевых аргументов переменной длинны

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

> Весь код функции можно вставить в ipython с помощью команды %cpaste.

Она берет файл с конфигурацией, убирает часть строк и возвращает остальные строки как список.

Попробуем вызывать её в ipython:
```python
In [4]: config_to_list('r1.txt')
Out[4]:
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
In [3]: config_to_list('r1.txt', delete_empty=False)
Out[3]:
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

> В этом примере, ```**kwargs``` используется и для того, чтобы указать, что функция clear_cfg_and_write_to_file может принимать аргументы переменной длинны, и для того, чтобы 'распаковать' словарь kwargs, котода мы передаем его в функцию config_to_list.

Так функция clear_cfg_and_write_to_file выглядит проще и понятней. И мы можем спокойно добавлять аргументы в функцию config_to_list, без необходимости дублировать их в функции clear_cfg_and_write_to_file.
