## Создание класса

Для создания классов в питоне используется ключевое слово `class`. Самый простой класс, который можно создать в Python:
```python
In [1]: class Switch:
   ...:     pass
   ...:
```

> Имена классов: в Python принято писать имена классов в формате CamelCase.

Для создания экземпляра класса, надо вызвать класс:
```python
In [2]: sw1 = Switch()

In [3]: print(sw1)
<__main__.Switch object at 0xb44963ac>
```

Создание переменных в экземпляре:
```python
In [5]: sw1.hostname = 'sw1'

In [6]: sw1.model = 'Cisco 3850'
```

В другом экземпляре класса Switch, переменные могут быть другие:
```python
In [7]: sw1 = Switch()

In [8]: sw2.hostname = 'sw2'

In [9]: sw2.model = 'Cisco 3750'
```

Посмотреть значение переменных экземпляра можно таким образом:
```python
In [10]: sw1.model
Out[10]: 'Cisco 3850'

In [11]: sw2.model
Out[11]: 'Cisco 3750'
```


### Методы

Для добавления метода, необходимо создать функцию внутри класса:
```python
In [15]: class Switch:
    ...:     def info(self):
    ...:         print('Hostname: {}\nModel: {}'.format(self.hostname, self.model))
    ...:
```

Тут появился загадочный self, с которым мы разберемся чуть позже, а пока демонстрация работы метода:
```python
In [16]: sw1 = Switch()

In [17]: sw1.hostname = 'sw1'

In [18]: sw1.model = 'Cisco 3850'

In [19]: sw1.info()
Hostname: sw1
Model: Cisco 3850
```

В примере выше сначала создается экземляр класса Switch, затем в экземпляр добавляются переменные hostname и model, и только после этого вызывается метод info.
Метод info выводит информацию про коммутатор, используя значения, которые хранятся в переменных экземпляра.

### Метод `__init__`

Для корректной работы метода info, необходимо чтобы у экземпляра были переменные hostname и model. Если этих переменных нет, возникнет ошибка:
```python
In [59]: sw2 = Switch()

In [60]: sw2.info()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-60-5a006dd8aae1> in <module>()
----> 1 sw2.info()

<ipython-input-57-30b05739380d> in info(self)
      1 class Switch:
      2     def info(self):
----> 3         print('Hostname: {}\nModel: {}'.format(self.hostname, self.model))

AttributeError: 'Switch' object has no attribute 'hostname'
```

Практически всегда, когда создается какой-то объект, у него есть какие-то начальные данные. Например, чтобы создать подключение к оборудование с помощью netmiko, надо передать параметры подключения.

В Python эти начальные данные про объект указываются в методе `__init__`. Метод `__init__` выполняется после того как Python создал новый экземпляр и, при этом, методу `__init__` передаются аргументы с которыми был создан экземпляр:
```python
In [32]: class Switch:
    ...:     def __init__(self, hostname, model):
    ...:         self.hostname = hostname
    ...:         self.model = model
    ...:
    ...:     def info(self):
    ...:         print('Hostname: {}\nModel: {}'.format(self.hostname, self.model))
    ...:
```

> Метод `__init__` иногда называют конструктором класса, хотя технически в Python сначала выполняется метод `__new__`, а затем `__init__`. В большинстве случаев, метод `__new__` использовать не нужно.

Теперь, при создании экземпляра класса Switch, обязательно надо указать hostname и model:
```python
In [33]: sw1 = Switch('sw1', 'Cisco 3850')
```

И, соответственно, метод info отрабатывает без ошибок:
```
In [36]: sw1.info()
Hostname: sw1
Model: Cisco 3850
```

### self



Эти варианты равнозначны:
```python
In [38]: Switch.info(sw1)
Hostname: sw1
Model: Cisco 3850

In [39]: sw1.info()
Hostname: sw1
Model: Cisco 3850
```

### self

```python
In [40]: class Switch:
    ...:     def __init__(self, hostname, model):
    ...:         self.hostname = hostname
    ...:         self.model = model
    ...:

In [41]: def info(sw_obj):
    ...:     print('Hostname: {}\nModel: {}'.format(sw_obj.hostname, sw_obj.model))
    ...:

In [42]: sw1 = Switch('sw1', 'Cisco 3850')

In [43]: info(sw1)
Hostname: sw1
Model: Cisco 3850
```


