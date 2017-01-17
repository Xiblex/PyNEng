##Система управления пакетами pip
Для установки пакетов Python, которые понадобятся в курсе, будем использовать __pip__.

__pip__ - это инструмент для установки пакетов из Python Package Index. А точнее, система управления пакетами.

PyPi (Python Package Index) это репозиторий пакетов Python. Он похож на RubyGems (Ruby), CPAN (Perl).

Скорее всего, если у вас уже установлен Python, то установлен и pip.

Проверяем pip:
```bash
$ pip --version
pip 1.1 from /usr/lib/python2.7/dist-packages (python 2.7)
```

Если команда выдала ошибку, значит pip не установлен. Установить его можно так:
```bash
apt-get install python-pip
```

Пока что, pip нам нужен будет, в первую очередь, для того чтобы поставить virtualenv.


> По ссылке можно посмотреть самые популярные пакеты PyPi:
http://pypi-ranking.info/alltime
