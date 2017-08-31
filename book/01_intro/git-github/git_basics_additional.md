## Дополнительные возможности

### git diff

Команда git diff позволяет просмотреть разницу между различными состояниями.

Например, внесем изменения в файл README и .gitignore, но не будем добавлять их в репозиторий.
Команда git status показывает, что оба файла изменены:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_status_5.png)


Если дать команду git diff, она покажет внесенные изменения:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_diff.png)

То есть, команда git diff показывает, какие изменения были внесены с последнего коммита.

Если теперь добавить изменения в файлах и ещё раз выполнить команду git diff, она ничего не покажет:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_add_git_diff.png)

Чтобы показать отличия между staging и последним коммитом, надо добавить параметр --staged:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_diff_staged.png)

Закоммитим изменения:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_commit_2.png)

### git log

Иногда нужно посмотреть, когда были выполнены последние изменения.
В этом поможет команда git log:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_log.png)

По умолчанию команда показывает все коммиты, начиная с самого свежего.

С помощью дополнительных параметров можно не только посмотреть информацию о коммитах, но и какие изменения были внесены.
Флаг -p позволяет отобразить отличия, которые были внесены каждым коммитом:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_log_p.png)

Более короткий вариант вывода можно вывести с флагом ```--stat```:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_log_stat.png)


