## Модуль os

Модуль ```os``` позволяет работать с файловой системой, с окружением, управлять процессами.

Мы рассмотрим лишь несколько полезных возможностей.
За более полным описанием возможностей модуля, вы можете обратиться к [документации](https://docs.python.org/2/library/os.html) или [статье на сайте PyMOTW](https://pymotw.com/2/os/index.html).

Модуль os позволяет создавать каталоги:
```python
In [1]: import os

In [2]: os.mkdir('test')

In [3]: ls -ls
total 0
0 drwxr-xr-x  2 nata  nata  68 Jan 23 18:58 test/
```

Кроме того, в модуле есть соответствующие проверки на существование.
Например, если попробовать повторно создать каталог, возникнет ошибка:
```python
In [4]: os.mkdir('test')
---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)
<ipython-input-4-cbf3b897c095> in <module>()
----> 1 os.mkdir('test')

OSError: [Errno 17] File exists: 'test'
```

В таком случае, пригодится проверка ```os.path.exists```:
```python
In [5]: os.path.exists('test')
Out[5]: True

In [6]: if not os.path.exists('test'):
   ...:     os.mkdir('test')
   ...:
```

Метод listdir, позволяет посмотреть содержимое каталога:
```python
In [7]: os.listdir('.')
Out[7]: ['cover3.png', 'dir2', 'dir3', 'README.txt', 'test']
```

С помощью проверок ```os.path.isdir``` и ```os.path.isfile```, можно получить отдельно список файлов и список каталогов:
```python
In [8]: dirs = [ d for d in os.listdir('.') if os.path.isdir(d)]

In [9]: dirs
Out[9]: ['dir2', 'dir3', 'test']

In [10]: files = [ f for f in os.listdir('.') if os.path.isfile(f)]

In [11]: files
Out[11]: ['cover3.png', 'README.txt']

```

Также в модуле есть отдельные методы для работы с путями:
```python
In [12]: os.path.basename(file)
Out[12]: 'README.md'

In [13]: os.path.dirname(file)
Out[13]: 'Programming/PyNEng/book/16_additional_info'

In [14]: os.path.split(file)
Out[14]: ('Programming/PyNEng/book/16_additional_info', 'README.md')
```
