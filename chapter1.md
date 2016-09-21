# Подготовка к работе

## ОС и редактор

Для того, чтобы начать работать с Python, надо определиться с несколькими вещами:
* Какая операционная система будет использоваться
* Какой редактор будет использоваться
* Какая версия Python будет использоваться

Можно выбрать любую ОС и любой редактор. Но, желательно использовать Python версии 2.7, так как в этом курсе будет использоваться эта версия.

__В курсе используются:__
* Debian Linux
* vim (редактор не имеет принципиального значения, лучше выбрать наиболее удобный)
* Python 2.7

> Установка Python 2.7, если его нет в ОС, выполняется самостоятельно.


Если вы не знаете какой редактор выбрать, попробуйте первый из списка для вашей ОС (vi/vim не указаны):
* Linux:
 * gEdit
 * nano
 * Sublime Text
 * geany
* Mac OS
 * TextWrangler
 * TextMate
* Windows:
 * Notepad++


> Далее выводы команд, интерпретатора, скриптов, выполняются на Debian Linux.
В других ОС вывод может незначительно отличаться.


## Система управления пакетами pip
Для установки пакетов Python, которые понадобятся в курсе, будем использовать __pip__.

__pip__ - это инструмент для установки пакетов из Python Package Index. А точнее, система управления пакетами.

PyPi (Python Package Index) это репозиторий пакетов Python. Он похож на RubyGems (Ruby), CPAN (Perl).

Скорее всего, если у вас уже установлен Python, то установлен и pip.

Проверяем pip:
```bash
nata@lab1:~$ pip --version
pip 1.1 from /usr/lib/python2.7/dist-packages (python 2.7)
```

Если команда выдала ошибку, значит pip не установлен. Установить его можно так:
```bash
apt-get install python-pip
```

Пока что, pip нам нужен будет, в первую очередь, для того чтобы поставить virtualenv.


> По ссылке можно посмотреть самые популярные пакеты PyPi:
http://pypi-ranking.info/alltime



## virtualenv, virtualenvwrapper
Для того чтобы то, что мы будем делать на курсе, не повлияло на вашу систему в целом, мы будем использовать __virtualenv__.

__virtualenv__ это инструмент, который позволяет создавать виртуальные окружения. 

Виртуальные окружения:
* позволяют изолировать различные проекты
* зависимости, которых требуют разные проекты, находятся в разных местах
 * Например, если в проекте 1 требуется пакет версии 1.0, а в проекте 2 требуется тот же пакет, но версии 3.1
* пакеты, которые установлены в виртуальных окружениях, не перебивают глобальные пакеты

Мы будем использовать __virtualenvwrapper__: он позволяет немного проще работать с virtualenv.

Устанавливаем virtualenvwrapper с помощью pip:
```
pip install virtualenvwrapper
```

В .bashrc надо добавить несколько строк (WORKON_HOME расположение виртуальных окружений; вторая строка - где находится скрипт, установленный с пакетом virtualenvwrapper):
```
export WORKON_HOME=~/venv

. /usr/local/bin/virtualenvwrapper.sh
```

#### Работа с виртуальными окружениями
Создание нового виртуального окружения:
```
nata@lab1:~$ mkvirtualenv Py_for_NetEng
New python executable in Py_for_NetEng/bin/python
Installing distribute........................done.
Installing pip...............done.
(Py_for_NetEng)nata@lab1:~$ 
```

Теперь в скобках перед стандартным приглашением пишется имя проекта (виртуального окружения).
То есть, мы не только создали новое виртуальное окружение, но и перешли в него.


> В virtualenvwrapper по Tab работает автопродолжение имени виртуального окружения. 

> Это особенно удобно в тех случаях, когда виртуальных окружений много.


Теперь в том каталоге, который был указан в WORKON_HOME, создан каталог Py_for_NetEng:
```
(Py_for_NetEng)nata@lab1:~$ ls -ls venv
total 52
....
4 -rwxr-xr-x 1 nata nata   99 Sep 30 16:41 preactivate
4 -rw-r--r-- 1 nata nata   76 Sep 30 16:41 predeactivate
4 -rwxr-xr-x 1 nata nata   91 Sep 30 16:41 premkproject
4 -rwxr-xr-x 1 nata nata  130 Sep 30 16:41 premkvirtualenv
4 -rwxr-xr-x 1 nata nata  111 Sep 30 16:41 prermvirtualenv
4 drwxr-xr-x 6 nata nata 4096 Sep 30 16:42 Py_for_NetEng
```

Выйти из виртуального окружения:
```
(Py_for_NetEng)nata@lab1:~$ deactivate 
nata@lab1:~$ 
```

Теперь для перехода в созданное виртуальное окружение надо выполнить команду __workon__:
```
nata@lab1:~$ workon Py_for_NetEng
(Py_for_NetEng)nata@lab1:~$ 
```

Если необходимо перейти из одного виртуального окружения в другое, то необязательно делать __deactivate__, можно перейти сразу через workon:
```
nata@lab1:~$ workon Test
(Test)nata@lab1:~$ workon Py_for_NetEng
(Py_for_NetEng)nata@lab1:~$ 
```

Если виртуальное окружение нужно удалить, используется команда __rmvirtualenv__:
```
nata@lab1:~$ rmvirtualenv Test
Removing Test...
nata@lab1:~$ 
```

Посмотреть какие пакеты установлены в виртуальном окружении:
```
(Py_for_NetEng)nata@lab1:~$ lssitepackages
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

Установим, к примеру, в нашем виртуальном окружении какой-то пакет (тут на примере simplejson). 

Теперь если перейти в ipython (рассматривается ниже) и импортировать simplejson, то он доступен и никаких ошибок нет:
```python
(Py_for_NetEng)nata@lab1:~$ pip install simplejson
...
Successfully installed simplejson
Cleaning up...

(Py_for_NetEng)nata@lab1:~$ ipython

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

Но, если выйти из виртуально окружения, и попытаться сделать то же самое, то такого модуля нет:
```python
(Py_for_NetEng)nata@lab1:~$ deactivate 

nata@lab1:~$ ipython

In [1]: import simplejson
------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
<ipython-input-1-ac998a77e3e2> in <module>()
----> 1 import simplejson

ImportError: No module named simplejson
```

## Интерпретатор Python (проверка)
Проверяем перед началом работы, что при вызове интерпретатора Python, вывод будет таким:
```python
nata@lab1:~$ python
Python 2.7.3 (default, Mar 13 2014, 11:03:55) 
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Вывод показывает, что установлен Python 2.7. Приглашение __>>>__ это стандартное приглашение интерпретатора Python.

Вызов интерпретатора выполняется по команде __python__, чтобы выйти нужно набрать __quit()__ либо нажать __Ctrl+D__