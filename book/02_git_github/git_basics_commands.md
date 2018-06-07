## Работа с Git

### git status

При работе с git, важно понимать текущий статус репозитория.

Для этого в Git есть команда git status:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_status_0.png)


Git сообщает, что мы находимся в ветке master (эта ветка создается сама и используется по умолчанию), и что ему нечего добавлять в коммит.
Кроме этого, git предлагает создать или скопировать файлы и после этого воспользоваться командой git add, чтобы git начал за ними следить.

Создание файла README и добавление в него строки "test":
```
$ vi README
```

> Можно сделать то же самое таким образом ```$ echo "test" >> README```.

После этого приглашение выглядит таким образом:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/bash_prompt.png)


В приглашении показано, что есть два файла, за которыми git еще не следит:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_status_1.png)

Два файла получились из-за того, что у меня настроены undo файлы для vim.
Это специальные файлы, благодаря которым можно отменять изменения не только в текущем открытии файла, но и прошлые.


Обратите внимание, что git сообщает, что есть файлы, за которыми он не следит и подсказывает, какой командой это сделать.

### .gitignore

.README.un~ - это служебный файл, который не нужно добавлять в репозиторий.

В git есть возможность сказать, что какие-то файлы или каталоги нужно игнорировать.
Для этого надо указать соответствующие шаблоны в файле .gitignore в текущем каталоге:

Для того, чтобы git игнорировал undo файлы vim, можно добавить, например, такую строку в файл .gitignore:
```
*.un~
```

Это значит, что Git должен игнорировать все файлы, которые заканчиваются на ```.un~```.

После этого git status показывает:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_status_2.png)


Обратите внимание, что теперь в выводе нет файла .README.un~.
Как только в репозитории добавлен файл .gitignore, файлы, которые указаны в нём, игнорируются.

### git add

Для того, чтобы Git начал следить за файлами, используется команда git add.

Можно указать, что надо следить за конкретным файлом:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_add_readme.png)

Или за всеми файлами:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_add_all.png)


Вывод git status:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_status_3.png)


Теперь файлы находятся в секции "Changes to be committed".

### git commit

После того, как все нужные файлы были добавлены в staging, можно закоммитить изменения.

У команды git commit есть только один обязательный параметр - флаг ```-m```.
Он позволяет указать сообщение для этого коммита:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_commit_1.png)


После этого git status отображает:

![alt](https://raw.githubusercontent.com/natenka/PyNEng/master/images/git/git_status_4.png)


Фраза "working directory clean" обозначает, что нет изменений, которые нужно добавить в Git или закоммитить.


