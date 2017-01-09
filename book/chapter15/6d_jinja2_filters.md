## Фильтры Jinja2

Ansible позволяет использовать фильтры Jinja2 не только в шаблонах, но и в playbook.

С помощью можно преобразовывать значения переменных, переводить их в другой формат и др.

Ansible поддерживает не только встроенные фильтры Jinja, но и множество собственных фильтров.
Мы не будем рассматривать все фильтры, поэтому, если вы не найдете нужный вам фильтр тут, посмотрите [документацию](http://docs.ansible.com/ansible/playbooks_filters.html).

Мы уже использовали фильтры:
* to_nice_json в разделе [ios_facts](https://natenka.gitbooks.io/pyneng/content/book/chapter15/4b_ios_facts.html)
* regex_findall в разделе [роли](https://natenka.gitbooks.io/pyneng/content/book/chapter15/6c_roles.html)

> Если вас интересуют фильтры Jinja2 в контексте использования их в шаблонах, это рассматривалось в разделе [Фильтры](https://natenka.gitbooks.io/pyneng/content/book/chapter13/3d_syntax_filter.html).

Для начала, перечислим несколько фильтров для общего понимания возможностей.

Ansible поддерживает такие фильтры (список не полный):
* [фильтры для форматирования данных](http://docs.ansible.com/ansible/playbooks_filters.html#filters-for-formatting-data):
 * ```{{ var | to_nice_json }}``` - преобразует данные в формат JSON
 * ```{{ var | to_nice_yaml }}``` - преобразует данные в формат YAML
* переменные
 * ```{{ var | default(9) }}``` - позволяет определить значение по умолчанию для переменной
 * ```{{ var | default(omit) }}``` - позволяет пропустить переменную, если она не определена
* списки
 * ```{{ lista | min }}``` - минимальный элемент списка
 * ```{{ lista | max }}``` - максимальный элемент списка
* [фильтры, которые работают множествами](http://docs.ansible.com/ansible/playbooks_filters.html#set-theory-filters)
 * ```{{ list1 | unique }}``` - возвращает множество уникальных элементов из списка
 * ```{{ list1 | difference(list2) }}``` - разница между двумя списками: каких элементов первого списка нет во втором
* [фильтр для работы с IP-адресами](http://docs.ansible.com/ansible/playbooks_filters_ipaddr.html)
 * ```{{ var | ipaddr }}``` - проверяет является ли переменная IP-адресом
* регулярные выражения
 * regex_replace - замена в строке
 * regex_search - ищет первое совпадение с регулярным выражением
 * regex_findall - ищет все совпадения с регулярным выражением
