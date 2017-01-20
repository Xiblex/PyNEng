## Параметры и аргументы функций

Цель создания функции, как правило, заключается в том, чтобы вынести кусок кода, который выполняет определенную задачу, в отдельный объект.
Это позволяет нам использовать этот кусок кода многократно, не создавая его заново в программе.

Как правило, функция должна выполнять какие-то действия с входящими значениями и на выходе выдавать результат.

Иногда, термины параметр и аргумент используются взаимозаменяемо. Тем не менее, это разные вещи:
* __параметры__ - это переменные, которые используются, при создании функции.
* __аргументы__ - это фактические значения (данные), которые передаются функции, при вызове.

Для того чтобы функция могла принимать входящие значения, мы должны ее создать с параметрами:
```python
In [1]: def delete_exclamation_from_cfg( in_cfg, out_cfg ):
   ...:     with open(in_cfg) as in_file:
   ...:         result = in_file.readlines()
   ...:     with open(out_cfg, 'w') as out_file:
   ...:         for line in result:
   ...:             if not line.startswith('!'):
   ...:                 out_file.write(line)
   ...:
```

В данном случае, у функции delete_exclamation_from_cfg два параметра: in_cfg и out_cfg.

Функция открывает файл in_cfg, читает содержимое в список; затем открывает файл out_cfg и записывает в него только те строки, которые не начинаются на знак восклицания.

В данном случае функция ничего не возвращает.

Файл r1.txt будем использовать как первый аргумент (in_cfg):
```python
In [2]: cat r1.txt
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
```

Попробуем использовать функцию delete_exclamation_from_cfg:
```python
In [3]: delete_exclamation_from_cfg('r1.txt', 'result.txt')
```

Файл result.txt выглядит так:
```python
In [4]: cat result.txt
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
no ip domain lookup
ip ssh version 2

```

При таком определении функции, мы обязаны передать оба аргумента. Если мы передадим только один аргумент, возникнет ошибка (как и в случае, если мы передадим 3 и больше аргументов):

```python
In [5]: delete_exclamation_from_cfg('r1.txt')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-7-66ae381f1c4f> in <module>()
----> 1 delete_exclamation_from_cfg('r1.txt')

TypeError: delete_exclamation_from_cfg() takes exactly 2 arguments (1 given)
```

