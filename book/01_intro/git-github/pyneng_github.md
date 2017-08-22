## Работа с репозиторием заданий и примеров

Все примеры и задания книги выложены в отдельном [репозитории](https://github.com/natenka/pyneng-examples-exercises).


### Копирование репозитория с GitHub

Примеры и задания периодически обновляются.
Поэтому будет удобней скопировать локально этот репозиторий и обновлять его, когда были внесены какие-то изменения.

Для копирования репозитория с GitHub, выполните команду git clone:
```
$ git clone https://github.com/natenka/pyneng-examples-exercises
Cloning into 'pyneng-examples-exercises'...
remote: Counting objects: 1263, done.
remote: Compressing objects: 100% (504/504), done.
remote: Total 1263 (delta 735), reused 1263 (delta 735), pack-reused 0
Receiving objects: 100% (1263/1263), 267.10 KiB | 444.00 KiB/s, done.
Resolving deltas: 100% (735/735), done.
Checking connectivity... done.

```

### Обновление локальной копии репозитория

При необходимости обновить локальную версию репозитория, чтобы синхронизировать её с версией на GitHub, надо выполнить git pull внутри созданного каталога pyneng-examples-exercises.

Если обновлений не было, вывод будет таким:
```
$ cd pyneng-examples-exercises/

$ git pull
Already up-to-date.
```

Если обновления были, вывод будет примерно таким:
```
$ git pull
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 3 (delta 2), reused 3 (delta 2), pack-reused 0
Unpacking objects: 100% (3/3), done.
From https://github.com/natenka/pyneng-examples-exercises
   49e9f1b..1eb82ad  master     -> origin/master
Updating 49e9f1b..1eb82ad
Fast-forward
 README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Обратите внимание на информацию о том, что изменился только файл README.md.

### Просмотр изменений

Если вы хотите посмотреть какие именно изменения были внесены, можно воспользоваться командой git log:
```
$ git log -p -1
commit 98e393c27e7aae4b41878d9d979c7587bfeb24b4
Author: Наташа Самойленко <nataliya.samoylenko@gmail.com>
Date:   Fri Aug 18 17:32:07 2017 +0300

    Update task_15_4.md

diff --git a/exercises/15_ansible/task_15_4.md b/exercises/15_ansible/task_15_4.md
index c4307fa..137a221 100644
--- a/exercises/15_ansible/task_15_4.md
+++ b/exercises/15_ansible/task_15_4.md
@@ -13,11 +13,12 @@
 * применить ACL к интерфейсу

 ACL должен быть таким:
+```
 ip access-list extended INET-to-LAN
  permit tcp 10.0.1.0 0.0.0.255 any eq www
  permit tcp 10.0.1.0 0.0.0.255 any eq 22
  permit icmp any any
-
+```

 Проверьте работу playbook на маршрутизаторе R1.

```

В этой команде флаг ```-p``` указывает, что мы хотим посмотреть diff изменений, а не только сообщение commit, а ```-1``` указывает, что надо показать только один commit (самый свежий).

### Посмотреть, какие изменения будут синхронизированы

Прошлый вариант опирается на количество коммитов.
Но это не всегда удобно.
До выполнения команды git pull, можно посмотреть какие изменения были выполнены с момента последней синхронизации.
Для этого используется такая команда:

```
$ git log -p ..origin/master
commit 4c1821030d20b3682b67caf362fd777d098d9126
Author: Наташа Самойленко <nataliya.samoylenko@gmail.com>
Date:   Mon May 29 07:53:45 2017 +0300

    Update README.md

diff --git a/tools/README.md b/tools/README.md
index 2b6f380..4f8d4af 100644
--- a/tools/README.md
+++ b/tools/README.md
@@ -1 +1,4 @@
 ## Инструменты
+
+Тут находятся PDF версии руководств по настройке инструментов, которые используются на курсе.
```

В данном случае, изменения были только в одном файле.

Эта команда будет очень полезна для того чтобы посмотреть, например, какие изменения были внесены в формулировку заданий и каких именно заданий.
Так будет легче сориентироваться касается ли это заданий, которые вы уже сделали и надо ли что-то изменить.

Если изменения были в тех заданиях, которые вы ещё не делали, этот вывод подскажет какие файлы нужно скопировать с репозитория курса в ваш личный репозиторий (а может и весь раздел, если вы еще не делали задания из этого раздела).

> ```..origin/master``` в этой команде означает показать все коммиты, которые есть в origin/master (в данном случае, это GitHub), но которых нет в вашей локальной копии репозитория.

