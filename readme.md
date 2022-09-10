Для запуска контейнера следует в корне проекта ввести следующую команду в командной строке:

'''
docker-compose up -d --build
'''

Далее для миграций и статики следует выполнить следующие команды:

'''
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input --clear
'''

Сервис будет доступен по адресу http://localhost