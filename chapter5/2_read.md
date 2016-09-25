## Чтение файлов
В Python есть несколько методов чтения файла:
* ```read()``` - этот метод считывает содержимое файла в строку
* ```readline()``` - считывает файл построчно
* ```readlines()``` - этот метод считывает строки файла и создает список из строк


####```read()```
Пример использования метода read():
```python
In [1]: f = open('test.txt')

In [2]: f.read()
Out[2]: 'This is line 1\nanother line\none more line\n'

In [3]: f.read()
Out[3]: ''
```

Комментарии к примеру:
* метод read() считал весь файл в одну строку
* в строке 3 метод read() вызван еще раз, но он уже возвращает пустую строку

####```readline()```
Построчно файл можно считать с помощью метода readline():
```python
In [4]: f = open('test.txt')

In [5]: f.readline()
Out[5]: 'This is line 1\n'

In [6]: f.readline()
Out[6]: 'another line\n'
```

Но, чаще всего, проще пройтись по объекту file в цикле:
```python
In [7]: f = open('test.txt')

In [8]: for line in f:
   ....:     print line
   ....:     
This is line 1

another line

one more line
```

####```readlines()```

Еще один полезный метод - readlines(). Он считывает строки файла в список:
```python
In [9]: f = open('test.txt')

In [10]: f.readlines()
Out[10]: ['This is line 1\n', 'another line\n', 'one more line\n']
```

Если нужно получить строки файла, но без перевода строки в конце (так как, в данном случае, split() разделяет на основании разделителя '\n', то без предварительного метода rstrip(), мы получим список, в конце которого будет пустая строка):
```python
In [11]: f = open('test.txt')

In [12]: f.read().rsplit('\n')
Out[12]: ['This is line 1', 'another line', 'one more line', '']

In [13]: f = open('test.txt')

In [14]: f.read().rstrip().split('\n')
Out[14]: ['This is line 1', 'another line', 'one more line']
```
