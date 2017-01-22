## Конструкция with

> Конструкция with называется менеджер контекста.

В Python существует более удобный способ работы с файлами, чем те, что мы рассматривали ранее, который гарантирует закрытие файла автоматически: конструкция ```with```:
```python
In [1]: with open('r1.txt', 'r') as f:
  ....:     for line in f:
  ....:         print line
  ....:
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

Обратите внимание и на то, как мы считывали строки файла:
```python
for line in f:
    print line
```

То есть, нам не понадобилось использовать методы ```read```.
Если вам нужно работать с файлом построчно, то лучше использовать такой вариант.

В предыдущем выводе, между строками файла были лишние пустые строки, так как print добавляет ещё один перевод строки.

Мы можем или поставить запятую в конце выражения print или вызвать метод ```rstrip```, чтобы удалить символы перевода строки в конце строки файла:
```python
In [2]: with open('r1.txt', 'r') as f:
  ....:     for line in f:
  ....:         print line.rstrip()
  ....:
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

In [3]: f.closed
Out[3]: True

```


И, конечно же, с конструкцией ```with``` можно использовать не только такой построчный вариант считывания, все методы, которые мы рассматривали до этого, также работают:
```python
In [4]: with open('r1.txt', 'r') as f:
  ....:     print f.read()
  ....:
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

> Конструкция ```with``` может использоваться не только с файлами.

> Подробнее об этом можно почитать по ссылке: http://stackoverflow.com/questions/3012488/what-is-the-python-with-statement-designed-for


