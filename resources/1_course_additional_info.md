# Материалы по темам курса

Тут собраны ссылки по темам курса. Большая часть из них пересекаются с темами курса, но есть и дополнения. В любом случае, даже те, которые пересекаются полезно почитать.


## Модули


## Регулярные выражения

Сайт для проверки регулярных выражений:
* [regex101](https://regex101.com/)

* [Документация модуля re](https://docs.python.org/2/library/re.html)

## YAML, JSON, CSV

Документация:
* [YAML](http://pyyaml.org/wiki/PyYAMLDocumentation)
* [CSV](https://docs.python.org/2/library/csv.html)
* [JSON](https://docs.python.org/2/library/json.html)

## DB

* [Документация модуля sqlite3](https://docs.python.org/2/library/sqlite3.html)

## Telnet, SSH

Документация:
* [Telnetlib](https://docs.python.org/2/library/telnetlib.html)
* [Pexpect](https://pexpect.readthedocs.io/en/stable/)
* [Paramiko](http://docs.paramiko.org/en/2.0/)
* [Netmiko](https://pynet.twb-tech.com/blog/automation/netmiko.html)
* [threading](https://docs.python.org/2/library/threading.html)
* [multiprocessing](https://docs.python.org/2/library/multiprocessing.html)

## Jinja2
Статьи:
* [Network Configuration Templates Using Jinja2. Matt Oswalt](https://keepingitclassless.net/2014/03/network-config-templates-jinja2/)
* [Python And Jinja2 Tutorial. Jeremy Schulman](http://packetpushers.net/python-jinja2-tutorial/)
* [Configuration Generator with Python and Jinja2](https://codingnetworker.com/2015/09/configuration-generator-with-python-and-jinja2/)
* [Custom filters for a Jinja2 based Config Generator](https://codingnetworker.com/2015/10/custom-filters-jinja2-config-generator/)

Документация:
* [Документация Jinja2](http://jinja.pocoo.org/docs/dev/)


## TextFSM
Статьи:
* [Programmatic Access to CLI Devices with TextFSM. Jason Edelman (26.02.2015)](http://jedelman.com/home/programmatic-access-to-cli-devices-with-textfsm/) - основы TextFSM и идеи о развитии, которые легли в основу модуля ntc-ansible
* [Parse CLI outputs with TextFSM. Henry Ölsner (24.08.2015)](https://codingnetworker.com/2015/08/parse-cli-outputs-textfsm/) - пример использования TextFSM для разбора большого файла с выводом sh inventory. Подробнее объясняется синтаксис TextFSM
* [Creating Templates for TextFSM and ntc_show_command. Jason Edelman (27.08.2015)](http://jedelman.com/home/creating-templates-for-textfsm-and-ntc_show_command/) - подробнее рассматривается синтаксис TextFSM и показаны примеры использования модуля ntc-ansible (обратите внимание, что синтаксис модуля уже немного изменился)
* [TextFSM and Structured Data. Kirk Byers (22.10.2015)](https://pynet.twb-tech.com/blog/python/textfsm.html) - вводная статья о TextFSM. Тут не описывается синтаксис, но дается общее представление о том, что такое TextFSM и пример его использования

Документация:
* [Документация TextFSM](https://code.google.com/archive/p/textfsm/wikis)

Проекты, которые используют TextFSM:
* [Модуль ntc-ansible](https://github.com/networktocode/ntc-ansible)

Шаблоны TextFSM (из модуля ntc-ansible):
* [ntc-templates](https://github.com/networktocode/ntc-templates/tree/89c57342b47c9990f0708226fb3f268c6b8c1549/templates)
