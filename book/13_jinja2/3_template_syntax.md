{% raw %}
## Синтаксис шаблонов Jinja2

До сих пор, в примерах шаблонов Jinja2 использовалась только подстановка переменных.
Это самый простой и понятный пример использования шаблонов.
Мы использовали его, чтобы разобраться с тем, как работать с шаблонами.
В этом разделе мы разберемся какие ещё возможности поддерживает язык шаблонов.

В шаблонах Jinja2 можно использовать:
* переменные
* условия (if/else)
* циклы (for)
* фильтры - специальные встроенные методы, которые позволяют делать преобразования переменных
* тесты - используются для проверки соответствует ли переменная какому-то условию

Кроме того, Jinja поддерживает наследование между шаблонами.
А также позволяет добавлять содержимое одного шаблона в другой.

Мы разберемся с основами этих возможностей.
Подробнее о шаблонах Jinja2 можно почитать в [документации](http://jinja.pocoo.org/docs/dev/templates/).

> Все файлы, которые используются как примеры в этом подразделе, находятся в каталоге 3_template_syntax/


Для генерации шаблонов мы будем использовать скрипт cfg_gen.py
```python
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import yaml
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TEMPLATE_DIR, template = sys.argv[1].split('/')
VARS_FILE = sys.argv[2]

env = Environment(loader = FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
template = env.get_template(template)

vars_dict = yaml.load( open( VARS_FILE ) )

print template.render( vars_dict )
```

В строке
```
env = Environment(loader = FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
```

Параметр ```trim_blocks=True``` - удаляет первую пустую строку после блока конструкции, если установлено в True (по умолчанию False).

Также можно добавлять параметр ```lstrip_blocks=True``` - если установлено в True, пробелы и табы в начале строки удаляются (по умолчанию False).


Для того, чтобы посмотреть на результат, нам нужно вызвать скрипт и передать ему два аргумента:
* шаблон
* файл с переменными, в формате YAML

Результат будет выведен на стандартный поток вывода.

Пример запуска скрипта:
```
$ python cfg_gen.py templates/variables.txt data_files/vars.yml
```
{% endraw %}
