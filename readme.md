Для запуска контейнера следует в корне проекта ввести следующую команду в командной строке:

```
docker-compose up -d --build
```

Далее для миграций и статики следует выполнить следующие команды:

```
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input --clear
```

Для создания админа можно использовать команду 

```
docker-compose exec web python manage.py createsuperuser
```

Сервис будет доступен по адресу:
```
http://localhost
```

CRUD для картинок по адресу:
```
http://localhost/api/v1/gallery/images/
```

Для удаления всех картинок админом есть ручка:
```
http://localhost/api/v1/gallery/admin/images/
```

Инф-я об аккаунте на:
```
http://localhost/api/v1/account/me/
```

Для логина и регистрации:
```
http://localhost/api/v1/account/login/
http://localhost/api/v1/account/register/
```