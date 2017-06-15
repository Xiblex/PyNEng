## Параметры и аргументы функций

Цель создания функции, как правило, заключается в том, чтобы вынести кусок кода, который выполняет определенную задачу, в отдельный объект.
Это позволяет использовать этот кусок кода многократно, не создавая его заново в программе.

Как правило, функция должна выполнять какие-то действия с входящими значениями и на выходе выдавать результат.

При работе с функциями, важно различать:
* __параметры__ - это переменные, которые используются, при создании функции.
* __аргументы__ - это фактические значения (данные), которые передаются функции, при вызове.

> Код функций, которые используются в этом разделе, можно скопировать из файла func_params_args.py

Для того чтобы функция могла принимать входящие значения, ее нужно создать с параметрами:
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

Файл r1.txt будет использоваться как первый аргумент (in_cfg):
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

Пример использования функции delete_exclamation_from_cfg:
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

При таком определении функции, надо обязательно передать оба аргумента.
Если передать только один аргумент, возникнет ошибка. Аналогично, возникнет ошибка, если передать три и больше аргументов:
```python
In [5]: delete_exclamation_from_cfg('r1.txt')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-12-66ae381f1c4f> in <module>()
----> 1 delete_exclamation_from_cfg('r1.txt')

TypeError: delete_exclamation_from_cfg() missing 1 required positional argument: 'out_cfg'

```

