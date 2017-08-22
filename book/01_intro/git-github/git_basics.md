## Git

Git:

* распределенная система контроля версий
* широко используется
* выпущен под лицензией GNU GPL v2

Система контроля версий (Version Control System, VCS):

* отслеживает изменения в файлах
* хранит несколько версий одного файла
* позволяет откатить изменения
* знает кто и когда сделал изменения


Git хранит изменения как снимок (snapshot) всего репозитория.
Этот снимок выполняется после каждого коммита (commit).

![git]()

Файл в Git может быть в таких состояниях:

* committed - файл сохранен в локальной базе
* modified - файл был изменен, но еще не сохранен в локальной базе
* staged - файл отмечен на добавление в следующий commit


![git areas]()

Соответственно, есть три основные части проекта Git:

* каталог Git (.git) - тут хранятся метаданные и база данных объектов проект
* рабочий каталог -  копия определённой версии проекта
* область подготовленных файлов (staging area) - информация о том, что должно попасть в следующий commit

### Установка Git

Установка Git
```
$ sudo apt-get install git
```

### Первичная настройка Git

Для начала работы с Git необходимо указать имя и email пользователя, которые будут использоваться в commit:

```
$ git config --global user.name "username"
$ git config --global user.email "username.user@example.com"
```

Посмотреть настройки можно таким образом:
```
$ git config --list
```

### Инициализация репозитория

Создадим с нуля репозиторий Git.

Чтобы создать репозиторий Git с нуля, надо создать каталог, в котором он будет находиться:
```
[~/tools]
$ mkdir first_repo
```

И перейти в него:
```
[~/tools]
$ cd first_repo
```

Теперь, в новом каталоге необходимо дать команду git init:
```
[~/tools/first_repo]
$ git init
Initialized empty Git repository in /home/vagrant/tools/first_repo/.git/
```

После этой команды, в каталоге создается каталог .git, в котором содержится вся информация, которая необходима для работы Git.

### Отображение статуса репозитория в командной строке

> Это дополнительный функционал, который не требуется для работы с Git, но очень помогает в этом.

При работе с Git, очень удобно, когда вы сразу знаете находитесь вы в обычном каталоге или в репозитории Git.
И, кроме того, было бы хорошо понимать статус текущего репозитория.

Для этого нужно установить [специальную утилиту](https://github.com/magicmonty/bash-git-prompt), которая будет показывать статус репозитория.

Процесс установки достаточно прост.
Надо скопировать репозиторий в домашний каталог пользователя, под которым вы работаете:
```
cd ~
git clone https://github.com/magicmonty/bash-git-prompt.git .bash-git-prompt --depth=1
```

А затем добавить в конец файла ```~/.bashrc``` такие строки:
```
GIT_PROMPT_ONLY_IN_REPO=1
source ~/.bash-git-prompt/gitprompt.sh
```

Для того чтобы изменения применились, перезапустить bash:
```
exec bash
```

> В моей конфигурации приглашение командной строки разнесено на несколько строк, поэтому у вас оно будет отличаться. Главное, обратите внимание на то, что появляется дополнительная информация, при переходе в репозиторий.


Теперь, если вы находитесь в обычном каталоге, приглашение выглядит так:
```
[~]
vagrant@jessie-i386:
$ 
```

Если же перейти в репозиторий Git:

![setup](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/setup_prompt.png)

### Работа с Git

Перед добавлением файлов в репозиторий, посмотрим информацию о текущем состоянии репозитория.

__git status__

Для этого в Git есть команда git status:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_status_0.png)


Git сообщает, что мы находимся в ветке master (эта ветка создается сама и используется по умолчанию) и что ему нечего добавлять в коммит.
Кроме этого, git предлагает создать или скопировать файлы и после этого воспользоваться командой git add, чтобы git начал за ними следить.

Создадим первый файл README и добавим в него пару произвольных строк текста:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/vi_readme.png)


После этого приглашение выглядит таким образом:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/bash_prompt.png)


Почему-то в приглашении показано, что есть два файла, за которыми git еще не следит.
Посмотрим в git status откуда взялся второй файл:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_status_1.png)

Git сообщает, что есть файлы за которыми он не следит, подсказывает какой командой это сделать.

Два файла получились из-за того, что у меня настроены undo файлы для vim.
Это специальные файлы, благодаря которым, можно отменять изменения не только в текущем открытии файла, но и прошлые.

__.gitignore__

.README.un~ - это служебный файл, который не нужно добавлять в репозиторий.

В git есть возможность сказать, что какие-то файлы или каталоги нужно игнорировать.
Для этого, надо указать соответствующие шаблоны в файле .gitignore в текущем каталоге:

Для того чтобы git игнорировал undo файлы vim, можно добавить, например, такую строку в файл .gitignore:
```
*.un~
```

Это значит, что Git должен игнорировать все файлы, которые заканчиваются на ```.un~```.

После этого, git status показывает:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_status_2.png)


Обратите внимание, что теперь в выводе нет файла .README.un~.
Как только в репозитории добавлен файл .gitignore, файлы, которые указаны в нем, игнорируются.

__git add__

Для того чтобы Git начал следить за файлами, используется команда git add.

Можно указать, что надо следить за конкретным файлом:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_add_readme.png)

Или за всеми файлами:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_add_all.png)


Проверим как теперь выглядит вывод git status:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_status_3.png)


Теперь файлы находятся в секции "Changes to be committed".

__git commit__

После того как все нужные файлы были добавлены в staging, можно закоммитить изменения.

У команды git commit есть только один обязательный параметр - флаг ```-m```.
Он позволяет указать сообщение для этого коммита:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_commit_1.png)


После этого, git status отображает:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_status_4.png)


Фраза "working directory clean" обозначает, что нет изменений, которые нужно добавить в Git или закоммитить.


### Дополнительные возможности git

__git diff__

Команда git diff позволяет просмотреть разницу между различными состояниями.

Например, внесем изменения в файл README и .gitignore, но не будем добавлять их в репозиторий.
Команда git status показывает, что оба файла изменены:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_status_5.png)


Если дать команду git diff, она покажет внесенные изменения:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_diff.png)

То есть, команда git diff показывает какие изменения были внесены с последнего коммита.

Если теперь добавить изменения в файлах, и ещё раз выполнить команду git diff, она ничего не покажет:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_add_git_diff.png)

Чтобы показать отличия между staging и последним коммитом, надо добавить параметр --staged:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_diff_staged.png)

Закоммитим изменения:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_commit_2.png)

__git log__

Иногда нужно посмотреть когда были выполнены последние изменения.
В этом поможет команда git log:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_log.png)

По умолчанию команда показывает все коммиты, начиная с самого свежего.

С помощью дополнительных параметров, можно не только посмотреть информацию о коммитах, но и какие изменения были внесены.
Флаг -p позволяет отобразить отличия, которые были внесены каждым коммитом:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_log_p.png)

Более короткий вариант вывода можно вывести с флагом ```--stat```:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/git/git_log_stat.png)


