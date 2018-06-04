## Изменения в книге

### 28.11.2017 В задании 19.2b добавлены примеры команд с ошибками

### 15.11.2017 Примеры в разделах по Ansible проверены на Ansible версии 2.4.1

### 05.11.2017 Задания 20.2, 20.2a изменены. Задания 20.3, 20.3a удалены.

Задания 20.2, 20.2a переписаны, чтобы в них предполагалось использование concurrent.futures.
Задания 20.3, 20.3a удалены.

### 05.11.2017 Подразделы threading и multiprocessing перенесены в раздел [Дополнительная информация](https://natenka.gitbooks.io/pyneng/content/book/25_additional_info/threading_multiprocessing/)

В этих разделах рассматриваются только основы модулей threading и multiprocessing.
При этом, задача запуска функции в потоках и процессах намного проще решается в модуле concurrent.futures.
К тому же, при использовании concurrent.futures не надо переписывать существующий код.

На случай если задача будет более сложная и функционала concurrent.futures не хватит, оставлены основы  модулей threading и multiprocessing.
Конечно, этих основ недостаточно, чтобы решать более сложные задачи, но это неплохой старт.

### 21.10.2017 Подраздел list, dict, set comprehensions перенесён в [8 раздел](https://natenka.gitbooks.io/pyneng/content/book/08_python_basic_examples/x_comprehensions.html)

### 15.10.2017 Реорганизация книги

Книга разделена на главы:

* [Глава I. Основы Python](https://natenka.gitbooks.io/pyneng/content/book/Part_I.html)
* [Глава II. Повторное использование кода](https://natenka.gitbooks.io/pyneng/content/book/Part_II.html)
* [Глава III. Регулярные выражения](https://natenka.gitbooks.io/pyneng/content/book/Part_III.html)
* [Глава IV. Запись и передача данных](https://natenka.gitbooks.io/pyneng/content/book/Part_IV.html)
* [Глава V. Работа с сетевым оборудованием](https://natenka.gitbooks.io/pyneng/content/book/Part_V.html)
* [Глава VI. Ansible](https://natenka.gitbooks.io/pyneng/content/book/Part_VI.html)


Изменена нумерация разделов и некоторые разделы разбиты на части.
Названия разделов и нумерация заданий изменены соответственно в [репозитории pyneng-examples-exercises](https://github.com/natenka/pyneng-examples-exercises).

Изменения по разделам:

* Добавлен раздел [Примеры использования основ](https://natenka.gitbooks.io/pyneng/content/book/08_python_basic_examples/) - в нем показаны примеры на основе пройденных тем, а также находятся подразделы [Распаковка переменных](https://natenka.gitbooks.io/pyneng/content/book/08_python_basic_examples/variable_unpacking.html) и [List, dict, set comprehensions](https://natenka.gitbooks.io/pyneng/content/book/08_python_basic_examples/x_comprehensions.html)
* Подраздел о Git и GitHub вынесен в отдельный [раздел](https://natenka.gitbooks.io/pyneng/content/book/02_git_github/)
* Раздел функции разделен на две части: [Функции](https://natenka.gitbooks.io/pyneng/content/book/09_functions/) и [Полезные встроенные функции](https://natenka.gitbooks.io/pyneng/content/book/10_useful_functions/)
* Раздел модули разделен на две части: [Модули](https://natenka.gitbooks.io/pyneng/content/book/11_modules/) и [Полезные модули](https://natenka.gitbooks.io/pyneng/content/book/12_useful_modules/)
* Раздел Unicode перенесён в главу [Запись и передача данных](https://natenka.gitbooks.io/pyneng/content/book/Part_IV.html)

### 14.10.2017 В подраздел [Работа с файлами в формате CSV](https://natenka.gitbooks.io/pyneng/content/book/17_serialization/1_csv.html) добавлена информация о DictWriter


### 27.09.2017 Подраздел [Форматирование строк](https://natenka.gitbooks.io/pyneng/content/book/04_data_structures/4b_string_format.html) разделен на две части

Ранее примеры со старым и новым вариантом форматирования строк были перемешаны.
Теперь подраздел разделен на две части: сначала новый вариант форматирования строк, затем старый.

### 09.09.2017 У книги появился замечательный редактор Слава Скороход

Все правки редактора внесены.
Теперь ошибок и опечаток намного меньше.

### 01.09.2017 Версия книги для Python 3 стала основной

Все изменения описаны в [статье](https://natenka.github.io/pyneng/pyneng-book-updated-to-python-3.6/).

Содержимое книги обновлено до Python версии 3.6.
Все примеры, задания и содержимое книги протестированы.


