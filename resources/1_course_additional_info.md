# Материалы по темам курса

Тут собраны ссылки по темам курса.
Большая часть из них пересекаются с темами курса, но есть и дополнения.
В любом случае, даже те, которые пересекаются полезно почитать.


## Ссылки на статьи и другие ресурсы
### Основы Python

Книги по Python:
* [A Byte of Python](https://www.gitbook.com/book/swaroopch/byte-of-python/details)
 * [эта же книга на русском](http://wombat.org.ua/AByteOfPython/toc.html)
* [Python 101](https://leanpub.com/python_101)
* [Learn Python the Hard Way](https://learnpythonthehardway.org/book/)

Курсы по основам Python:
* [Программирование на Python](https://stepik.org/course/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BD%D0%B0-Python-67)

### Регулярные выражения

Статьи:
* [Parse Cisco IOS configurations using RegEx](https://codingnetworker.com/2016/05/parse-cisco-ios-configurations-regex/)
* [Using Python to generate Cisco configs](https://notalwaysthenetwork.com/2014/04/01/using-python-to-generate-cisco-configs/)

Сайт для проверки регулярных выражений:
* [regex101](https://regex101.com/)

### Базы данных

Более подробное описание возможностей SQLite:
* [SQLite tutorial](http://www.sqlitetutorial.net/)

### Telnet, SSH

Статьи:
* [Netmiko Library](https://pynet.twb-tech.com/blog/automation/netmiko.html)
* [Automate SSH connections with netmiko](https://codingnetworker.com/2016/03/automate-ssh-connections-with-netmiko/)
* [Network Automation Using Python: BGP Configuration](http://www.networkcomputing.com/networking/network-automation-using-python-bgp-configuration/1423704194)

### Jinja2

Статьи:
* [Network Configuration Templates Using Jinja2. Matt Oswalt](https://keepingitclassless.net/2014/03/network-config-templates-jinja2/)
* [Python And Jinja2 Tutorial. Jeremy Schulman](http://packetpushers.net/python-jinja2-tutorial/)
* [Configuration Generator with Python and Jinja2](https://codingnetworker.com/2015/09/configuration-generator-with-python-and-jinja2/)
* [Custom filters for a Jinja2 based Config Generator](https://codingnetworker.com/2015/10/custom-filters-jinja2-config-generator/)

### TextFSM
Статьи:
* [Programmatic Access to CLI Devices with TextFSM. Jason Edelman (26.02.2015)](http://jedelman.com/home/programmatic-access-to-cli-devices-with-textfsm/) - основы TextFSM и идеи о развитии, которые легли в основу модуля ntc-ansible
* [Parse CLI outputs with TextFSM. Henry Ölsner (24.08.2015)](https://codingnetworker.com/2015/08/parse-cli-outputs-textfsm/) - пример использования TextFSM для разбора большого файла с выводом sh inventory. Подробнее объясняется синтаксис TextFSM
* [Creating Templates for TextFSM and ntc_show_command. Jason Edelman (27.08.2015)](http://jedelman.com/home/creating-templates-for-textfsm-and-ntc_show_command/) - подробнее рассматривается синтаксис TextFSM и показаны примеры использования модуля ntc-ansible (обратите внимание, что синтаксис модуля уже немного изменился)
* [TextFSM and Structured Data. Kirk Byers (22.10.2015)](https://pynet.twb-tech.com/blog/python/textfsm.html) - вводная статья о TextFSM. Тут не описывается синтаксис, но дается общее представление о том, что такое TextFSM и пример его использования

Проекты, которые используют TextFSM:
* [Модуль ntc-ansible](https://github.com/networktocode/ntc-ansible)

Шаблоны TextFSM (из модуля ntc-ansible):
* [ntc-templates](https://github.com/networktocode/ntc-templates/tree/89c57342b47c9990f0708226fb3f268c6b8c1549/templates)


### Ansible

У Ansible очень хорошая документация:
- http://docs.ansible.com/ansible/

Отличные видео от Ansible:
* [AUTOMATING YOUR NETWORK](https://www.ansible.com/webinars-training/automating-your-network)
 * [Репозиторий с примерами из вебинара](https://github.com/privateip/Ansible-Webinar-Mar2016)

#### Ansible без привязки к сетевому оборудованию

Очень хорошая серия видео, с транскриптом и хорошими ссылками:
- https://sysadmincasts.com/episodes/43-19-minutes-with-ansible-part-1-4

Примеры использования Ansible:
- https://github.com/ansible/ansible-examples

Примеры Playbook с демонстрацией различных возможностей
- https://github.com/ansible/ansible-examples/tree/master/language_features


#### Ansible for network devices

> Обращайте внимание на время написания статьи. В Ansible существенно изменились модули для работы с сетевым оборудованием. И в статьях могут быть ещё старые примеры.

Network Config Templating using Ansible (Kirk Byers):
- https://pynet.twb-tech.com/blog/ansible/ansible-cfg-template.html
- https://pynet.twb-tech.com/blog/ansible/ansible-cfg-template-p2.html
- https://pynet.twb-tech.com/blog/ansible/ansible-cfg-template-p3.html

Статьи:
- http://jedelman.com/home/ansible-for-networking/
- http://jedelman.com/home/network-automation-with-ansible-dynamically-configuring-interface-descriptions/
- http://www.packetgeek.net/2015/08/using-ansible-to-push-cisco-ios-configurations/

Очень хорошая серия статей. Постепенно повышается уровень сложности:
- http://networkop.github.io/blog/2015/06/24/ansible-intro/
- http://networkop.github.io/blog/2015/07/03/parser-modules/
- http://networkop.github.io/blog/2015/07/10/test-verification/
- http://networkop.github.io/blog/2015/07/17/tdd-quickstart/
- http://networkop.github.io/blog/2015/08/14/automating-legacy-networks/
- http://networkop.github.io/blog/2015/08/26/automating-network-build-p1/
- http://networkop.github.io/blog/2015/09/03/automating-bgp-config/
- http://networkop.github.io/blog/2015/11/13/automating-flexvpn-config/


## Ссылки на документацию

Документация модулей, которые использовались в курсе:
* [re](https://docs.python.org/2/library/re.html)
* [YAML](http://pyyaml.org/wiki/PyYAMLDocumentation)
* [CSV](https://docs.python.org/2/library/csv.html)
* [JSON](https://docs.python.org/2/library/json.html)
* [sqlite3](https://docs.python.org/2/library/sqlite3.html)
* [Telnetlib](https://docs.python.org/2/library/telnetlib.html)
* [Pexpect](https://pexpect.readthedocs.io/en/stable/)
* [Paramiko](http://docs.paramiko.org/en/2.0/)
* [Netmiko](https://pynet.twb-tech.com/blog/automation/netmiko.html)
* [threading](https://docs.python.org/2/library/threading.html)
* [multiprocessing](https://docs.python.org/2/library/multiprocessing.html)
* [Jinja2](http://jinja.pocoo.org/docs/dev/)
* [TextFSM](https://github.com/google/textfsm/wiki)
* [Ansible](http://docs.ansible.com/ansible/)
