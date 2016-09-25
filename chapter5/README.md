#Работа с файлами

В работе с файлами есть несколько аспектов:
* открытие/закрытие
* чтение
* запись


## Чтение файлов
В Python есть несколько методов чтения файла:
* read() - этот метод считывает содержимое файла в строку
* readline() - считывает файл построчно
* readlines() - этот метод считывает строки файла и создает список из строк

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

## Запись файлов
При записи очень важно определиться с режимом открытия файла (чтобы случайно его не удалить):
* append - добавить строки в существующий файл
* write - перезаписать файл
* оба режима создают файл, если он не существует

Для записи в файл используются такие методы:
* write() - записать в файл одну строку
* writelines() - позволяет передавать в качестве аргумента список строк

Пример использования метода write():
```python
In [1]: f = open('test2.txt', 'a')
In [2]: f.write('line1\n')
In [3]: f.write('line2\n')
In [4]: f.write('line3\n')
In [5]: f.close()

In [6]: cat test2.txt
line1
line2
line3
```

Пример использования метода write() (обратите внимание, что файл перезаписался):
```python
In [8]: list1 = ['line4\n','line5\n','line6\n']

In [9]: f = open('test2.txt', 'w')
In [10]: f.writelines(list1)
In [11]: f.close()

In [12]: cat test2.txt
line4
line5
line6
```

## Конструкция with
При работе с файлами, надо не забывать закрывать файл, после выполненых операций.

Однако, в Python существует более удобный способ работы с файлами, который гарантирует закрытие файла автоматически: конструкция __with ... as__:
```python
In [13]: with open('test2.txt') as f:
   ....:     for line in f:
   ....:         print line
   ....:         
line4
line5
line6

In [14]: f.closed
Out[14]: True
```


> Эта конструкция может использоваться не только с файлами.

> Подробнее об этом можно почитать по ссылке: http://stackoverflow.com/questions/3012488/what-is-the-python-with-statement-designed-for


Нечто похожее можно сделать с конструкцией try/finally (плюс обрабатывать исключения):
```python
In [15]: try:
   ....:     f = open('test2.txt')
   ....: except IOError:
   ....:     print 'No such file'
   ....: finally:
   ....:     f.close()
   ....:     
In [16]: f.closed
Out[16]: True
```

Если такого файла нет:
```python
In [16]: try:
   ....:     f = open('test4.txt')
   ....: except IOError:
   ....:     print 'No such file'
   ....: finally:
   ....:     f.close()
   ....:     
No such file
```
