# -*- coding: utf-8 -*-

username = raw_input('Введите имя пользователя: ' )
password = raw_input('Введите пароль: ' )

pass_OK = False

while not pass_OK:
    if len(password) < 8:
        print 'Пароль слишком короткий\n'
        password = raw_input('Введите пароль еще раз: ' )
    elif username in password:
        print 'Пароль содержит имя пользователя\n'
        password = raw_input('Введите пароль еще раз: ' )
    else:
        print 'Пароль для пользователя %s установлен' % username
        pass_OK = True