# Материалы по темам курса

Тут собраны ссылки по темам курса. Большая часть из них пересекаются с темами курса, но есть и дополнения. В любом случае, даже те, которые пересеаются полезно почитать.

## Блоги

* [Kirk Byers](https://pynet.twb-tech.com/)
* [Jason Edelman](http://jedelman.com/)
* [Michael Kashin](http://networkop.co.uk/)
* [Henry Ölsner](https://codingnetworker.com/)

## Подкасты
* [Packet Pushers Show 176 – Intro To Python & Automation For Network Engineers](http://packetpushers.net/podcast/podcasts/show-176-intro-to-python-automation-for-network-engineers/)
* [Packet Pushers Show 198 – Kirk Byers On Network Automation With Python & Ansible](http://packetpushers.net/podcast/podcasts/show-198-kirk-byers-network-automation-python-ansible/)
* [Packet Pushers Show 270: Design & Build 9: Automation With Python And Netmiko](http://packetpushers.net/podcast/podcasts/show-270-design-build-9-automation-python-netmiko/)


## Курсы (платные и бесплатные).

> Я эти курсы не проходила, поэтому они собраны в произвольном порядке, просто чтобы было проще оценить, что есть на сегодняшний день и выбрать то, что больше нравится.

* [Бесплатный email курс от Kirk Byers](https://pynet.twb-tech.com/email-signup.html)
* [Платный курс от Kirk Byers](https://pynet.twb-tech.com/class.html)
* [Платные курсы от Jason Edelman](http://networktocode.com/products/training/)
* [Платный курс от INE](http://www.ine.com/self-paced/technologies/python-network-engineers.htm)
* [Новый курс по Ansible от INE (вероятно, он будет платный)](https://streaming.ine.com/c/ine-network-automation-with-ansible)
* [Платный курс на Udemy](https://www.udemy.com/python-programming-for-network-engineers/)
* [Платный курс на GNS3](http://academy.gns3.com/p/python-programming-for-real-life-networking-use)
* [Платный курс от ehacking academy](http://academy.ehacking.net/p/network-automation-python-engineers)


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
