## Материалы по темам курса

Тут собраны ссылки по темам курса. Большая часть из них пересекается с темами курса, но есть и дополнения. В любом случае, даже те, которые пересеаются полезно почитать.

## Обработка вывода команд с TextFSM

### TextFSM
Статьи:
* [Programmatic Access to CLI Devices with TextFSM. Jason Edelman (26.02.2015)](http://jedelman.com/home/programmatic-access-to-cli-devices-with-textfsm/) - основы TextFSM и идеи о развитии, которые легли в основы модуля ntc-ansible
* [Parse CLI outputs with TextFSM. Henry Ölsner (24.08.2015)](https://codingnetworker.com/2015/08/parse-cli-outputs-textfsm/) - пример использования TextFSM для разбора большого файла с выводом sh inventory. Подробнее объясняется синтаксис TextFSM
* [Creating Templates for TextFSM and ntc_show_command. Jason Edelman (27.08.2015)](http://jedelman.com/home/creating-templates-for-textfsm-and-ntc_show_command/) - подробнее рассматривается синтаксис TextFSM и показаны примеры использования модуля ntc-ansible (обратите внимание, что синтаксис модуля уже немного изменился)
* [TextFSM and Structured Data. Kirk Byers (22.10.2015)](https://pynet.twb-tech.com/blog/python/textfsm.html) - вводная статья о TextFSM. Тут не описывается синтаксис, но дается общее представление о том, что такое TextFSM и пример его использования

Документация:
* [Документация TextFSM](https://code.google.com/archive/p/textfsm/wikis)

Проекты, которые используют TextFSM:
* [Модуль ntc-ansible](https://github.com/networktocode/ntc-ansible)

Шаблоны TextFSM (из модуля ntc-ansible):
* [ntc-templates](https://github.com/networktocode/ntc-templates/tree/89c57342b47c9990f0708226fb3f268c6b8c1549/templates)
