## Виртуальные окружения

Виртуальные окружения:

* позволяют изолировать различные проекты
* зависимости, которые нужны разным проектам, находятся в разных местах - например, если в проекте 1 требуется пакет версии 1.0, а в проекте 2 требуется тот же пакет, но версии 3.1
* пакеты, которые установлены в виртуальных окружениях, не перебивают глобальные пакеты

Начиная с версии Python 3.5, рекомендуется использовать такой способ создания виртуальных окружений:
```
$ python3.6 -m venv new/pyneng
```

> Вместо python3.6 может использоваться python или python3, в зависимости от того, как установлен Python 3.6

Эта команда создает указанный каталог и все каталоги в пути, если они не были созданы.

Команда создает такую структуру каталогов:
```
$ ls -ls new/pyneng
total 16
4 drwxr-xr-x 2 vagrant vagrant 4096 Aug 21 14:50 bin
4 drwxr-xr-x 2 vagrant vagrant 4096 Aug 21 14:50 include
4 drwxr-xr-x 3 vagrant vagrant 4096 Aug 21 14:50 lib
4 -rw-r--r-- 1 vagrant vagrant   75 Aug 21 14:50 pyvenv.cfg
```

Для перехода в виртуальное окружение надо выполнить команду:
```
$ source new/pyneng/bin/activate
```

Для выхода из виртуального окружения используется команда deactivate:
```
$ deactivate
```

> [Подробнее о модуле venv](https://docs.python.org/3/library/venv.html#module-venv)

### virtualenvwrapper

Еще один вариант создания виртуальных окружений - virtualenvwrapper.
Он позволяет немного проще работать с виртуальными окружениями.

Установка virtualenvwrapper с помощью pip:
```
sudo pip install virtualenvwrapper
```

После установки в ```.bashrc``` нужно добавить несколько строк
```
export WORKON_HOME=~/venv

. /usr/local/bin/virtualenvwrapper.sh
```

> Если вы используете не bash, посмотрите, поддерживается ли ваш shell в [документации](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)

WORKON_HOME - указывает расположение виртуальных окружений.
А вторая строка - где находится скрипт, установленный с пакетом virtualenvwrapper.

Для того, чтобы скрипт virtualenvwrapper.sh выполнился и можно было работать с виртуальными окружениями, надо перезапустить bash. Например, таким образом:
```
exec bash
```


> Такой вариант может быть не всегда правильным. Подробнее в ответе на [stackoverflow](http://stackoverflow.com/questions/2518127/how-do-i-reload-bashrc-without-logging-out-and-back-in).

#### Работа с виртуальными окружениями

Создание нового виртуального окружения, в котором Python 3.6 используется по умолчанию:
```
$ mkvirtualenv --python=/usr/local/bin/python3.6 pyneng
New python executable in PyNEng/bin/python
Installing distribute........................done.
Installing pip...............done.
(pyneng)$ 
```

В скобках перед стандартным приглашением отображается имя проекта (виртуального окружения).
Это означает, что мы находимся в этом виртуальном окружении.


> В virtualenvwrapper по Tab работает автопродолжение имени виртуального окружения. 

> Это особенно удобно в тех случаях, когда виртуальных окружений много.


Теперь в том каталоге, который был указан в WORKON_HOME, создан каталог PyNEng:
```
(pyneng)$ ls -ls venv
total 52
....
4 -rwxr-xr-x 1 nata nata   99 Sep 30 16:41 preactivate
4 -rw-r--r-- 1 nata nata   76 Sep 30 16:41 predeactivate
4 -rwxr-xr-x 1 nata nata   91 Sep 30 16:41 premkproject
4 -rwxr-xr-x 1 nata nata  130 Sep 30 16:41 premkvirtualenv
4 -rwxr-xr-x 1 nata nata  111 Sep 30 16:41 prermvirtualenv
4 drwxr-xr-x 6 nata nata 4096 Sep 30 16:42 pyneng
```

Выйти из виртуального окружения:
```
(pyneng)$ deactivate 
$ 
```

Для перехода в созданное виртуальное окружение надо выполнить команду __workon__:
```
$ workon pyneng
(pyneng)$ 
```

Если необходимо перейти из одного виртуального окружения в другое, то необязательно делать __deactivate__, можно перейти сразу через workon:
```
$ workon Test
(Test)$ workon pyneng
(pyneng)$ 
```

Если виртуальное окружение нужно удалить, используется команда __rmvirtualenv__:
```
$ rmvirtualenv Test
Removing Test...
$ 
```

Посмотреть, какие пакеты установлены в виртуальном окружении:
```
(pyneng)$ lssitepackages
ANSI.py                                pexpect-3.3-py2.7.egg-info
ANSI.pyc                               pickleshare-0.5-py2.7.egg-info
decorator-4.0.4-py2.7.egg-info         pickleshare.py
decorator.py                           pickleshare.pyc
decorator.pyc                          pip-1.1-py2.7.egg
distribute-0.6.24-py2.7.egg            pxssh.py
easy-install.pth                       pxssh.pyc
fdpexpect.py                           requests
fdpexpect.pyc                          requests-2.7.0-py2.7.egg-info
FSM.py                                 screen.py
FSM.pyc                                screen.pyc
IPython                                setuptools.pth
ipython-4.0.0-py2.7.egg-info           simplegeneric-0.8.1-py2.7.egg-info
ipython_genutils                       simplegeneric.py
ipython_genutils-0.1.0-py2.7.egg-info  simplegeneric.pyc
path.py                                test_path.py
path.py-8.1.1-py2.7.egg-info           test_path.pyc
path.pyc                               traitlets
pexpect                                traitlets-4.0.0-py2.7.egg-info
```

### Зависимости (requirements)

При работе над проектом, в виртуальном окружении со временем находится всё больше установленных пакетов, и при необходимости поделиться проектом или скопировать его на другой сервер, нужно будет заново установить все зависимости.

В Python есть возможность (и принято) записать все зависимости в отдельный файл.

Это делается таким образом:
```
(pyneng)$ pip freeze > requirements.txt
```

Теперь в файле requirements.txt находятся все зависимости с версиями пакетов (файл requirements.txt):
```
Jinja2==2.8
pexpect==4.0.1
tornado==4.3
...
```

После этого, при необходимости установить все зависимости, надо перейти в новое виртуальное окружение, которое вы создали на сервере, или просто на новый сервер и дать команду:
```
$ pip install -r requirements.txt
```

> Тут в приглашении нет имени виртуального окружения, так как устанавливать таким образом зависимости можно не только в виртуальном окружении, но и в системе в целом.

### Установка пакетов

Например, установим в виртуальном окружении пакет simplejson. 
```
(pyneng)$ pip install simplejson
...
Successfully installed simplejson
Cleaning up...
```

Если перейти в ipython (рассматривается в разделе [ipython](../02_start/1_ipython.md)) и импортировать simplejson, то он доступен и никаких ошибок нет:
```
(pyneng)$ ipython

In [1]: import simplejson

In [2]: simplejson
simplejson

In [2]: simplejson.
simplejson.Decimal             simplejson.decoder
simplejson.JSONDecodeError     simplejson.dump
simplejson.JSONDecoder         simplejson.dumps
simplejson.JSONEncoder         simplejson.encoder
simplejson.JSONEncoderForHTML  simplejson.load
simplejson.OrderedDict         simplejson.loads
simplejson.absolute_import     simplejson.scanner
simplejson.compat              simplejson.simple_first
```

Но если выйти из виртуально окружения и попытаться сделать то же самое, то такого модуля нет:
```python
(pyneng)$ deactivate 

$ ipython

In [1]: import simplejson
------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
<ipython-input-1-ac998a77e3e2> in <module>()
----> 1 import simplejson

ImportError: No module named simplejson
```


