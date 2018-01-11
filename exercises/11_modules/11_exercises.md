# Задания

{% include "../exercises_intro.md" %}


### Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (а не имя файла).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
```
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0
```

Функция должна вернуть такой словарь:
```python
{('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
 ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
```

Интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.

Проверить работу функции на содержимом файла sw1_sh_cdp_neighbors.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.


### Задание 11.2

> Для выполнения этого задания, должен быть установлен graphviz:

> ```apt-get install graphviz```

> И модуль python для работы с graphviz:

> ```pip install graphviz```

С помощью функции parse_cdp_neighbors из задания 11.1
и функции draw_topology из файла draw_network_graph.py,
сгенерировать топологию, которая соответствует выводу
команды sh cdp neighbor в файле sw1_sh_cdp_neighbors.txt

Не копировать код функций parse_cdp_neighbors и draw_topology.

В итоге, должен быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_11_2_topology.svg

![task_8_2a_topology](https://raw.githubusercontent.com/natenka/PyNEng/master/images/08_modules/task_8_2a_topology.png)

При этом:
* Интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме

Ограничение: Все задания надо выполнять используя только пройденные темы.



### Задание 11.2a

> Для выполнения этого задания, должен быть установлен graphviz:

> ```apt-get install graphviz```

> И модуль python для работы с graphviz:

> ```pip install graphviz```

С помощью функции parse_cdp_neighbors из задания 11.1
и функции draw_topology из файла draw_network_graph.py,
сгенерировать топологию, которая соответствует выводу
команды sh cdp neighbor из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt


Не копировать код функций parse_cdp_neighbors и draw_topology.

В итоге, должен быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_11_2a_topology.svg

![task_8_2b_topology](https://raw.githubusercontent.com/natenka/PyNEng/master/images/08_modules/task_8_2b_topology.png)

При этом:
* Интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме

Ограничение: Все задания надо выполнять используя только пройденные темы.


