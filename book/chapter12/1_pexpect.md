## Модуль pexpect

Модуль pexpect позволяет автоматизировать интерактивные подключения, такие как:
* telnet
* ssh
* ftp

> Pexpect это реализация инструмента expect на Python.

Логика работы pexpect такая:
* запускаем какую-то программу
* ожидаем определенный вывод (приглашение, запрос пароля и подобное)
* отправляем команды/данные
* последние два действия повторяются столько, сколько нужно

Очень важно понимать, что сам pexpect не реализует различные утилиты, а использует уже готовые.

В Pexpect есть два основных инструмента:
* функция run()
* класс spawn

### pexpect.run()

Функция run() позволяет легко вызвать какую-то программу и вернуть её вывод.

Например:
```python
In [1]: import pexpect

In [2]: output = pexpect.run('ls -ls')

In [3]: print output
total 368
  8 -rw-r--r--   1 natasha  staff     372 Sep 26 08:36 LICENSE.md
  8 -rw-r--r--   1 natasha  staff    3483 Sep 26 08:36 README.md
 16 -rw-r--r--   1 natasha  staff    7098 Oct  5 11:41 SUMMARY.md
  8 -rw-r--r--   1 natasha  staff      70 Sep 25 19:01 about.md
  0 drwxr-xr-x  17 natasha  staff     578 Sep 25 19:05 book
  8 -rw-r--r--   1 natasha  staff     239 Sep 27 06:32 book.json
288 -rw-r--r--   1 natasha  staff  146490 Sep 27 09:11 cover.jpg
  0 drwxr-xr-x   6 natasha  staff     204 Sep 25 19:01 exercises
 24 -rw-r--r--   1 natasha  staff   10024 Sep 25 19:01 faq.md
  0 drwxr-xr-x   3 natasha  staff     102 Sep 27 16:25 resources
  8 -rw-r--r--   1 natasha  staff    3633 Sep 27 15:52 schedule.md
```

### pexpect.spawn

Класс spawn поддерживает больше возможностей. Он позволяет взаимодействовать с вызванной программой, отправляя данные и ожидая ответ.

Простой пример использования pexpect.spwan:
```python
t = pexpect.spawn('ssh user@10.1.1.1')

t.expect('Password:')
t.sendline("userpass")
t.expect('>')
```

Тут мы подключаемся по SSH, и ожидаем строку 'Password:'. Как только она появилась, отправляем пароль. Затем ждем строку '>'.


