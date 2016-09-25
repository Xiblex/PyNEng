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
