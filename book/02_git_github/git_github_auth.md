### Аутентификация на GitHub

Для того, чтобы начать работать с GitHub, надо на нём [зарегистрироваться](https://github.com/join). Для безопасной работы с GitHub лучше использовать аутентификацию по ключам SSH.

> Такая же [инструкция](https://help.github.com/articles/connecting-to-github-with-ssh/) на GitHub

Генерация нового SSH ключа (используйте email, который привязан к GitHub):

```shellsession
$ ssh-keygen -t rsa -b 4096 -C "github_email@gmail.com"
```

На всех вопросах достаточно нажать Enter (более безопасно использовать ключ с passphrase, но можно и без, если нажать Enter при вопросе, тогда passphrase не будет запрашиваться у Вас постоянно при операциях с репозиторием).

Запуск SSH-агента:

```shellsession
$ eval "$(ssh-agent -s)"
```

Добавить ключ в SSH-агент:

```shellsession
$ ssh-add ~/.ssh/id_rsa
```

#### Добавление SSH-ключа на GitHub

Для добавления ключа надо его скопировать.

Например, таким образом можно отобразить ключ для копирования:

```shellsession
$ cat ~/.ssh/id_rsa.pub
```

После копирования надо перейти на GitHub. Находясь на любой странице GitHub, в правом верхнем углу нажмите на картинку вашего профиля и в выпадающем списке выберите "Settings". В списке слева надо выбрать поле "SSH and GPG keys". После этого надо нажать "New SSH key" и в поле "Title" написать название ключа (например "Home"), а в поле "Key" вставить содержимое, которое было скопировано из файла ~/.ssh/id_rsa.pub.

> Если GitHub запросит пароль, введите пароль своего аккаунта на GitHub

Чтобы проверить, что всё прошло успешно, попробуйте выполнить команду ssh -T git@github.com.

Вывод должен быть таким:

```shellsession
$ ssh -T git@github.com
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

Теперь Вы готовы работать с Git и GitHub.
