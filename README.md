![example event parameter](https://github.com/kaspeya/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)
# FoodGram ( docker-compose )

#### Проект доступен по ссылке:

[КЛИК](http://62.84.119.109/)<br/>
[API](http://62.84.119.109/api/)<br/>
[Документация в формате ReDoc](http://62.84.119.109/api/docs/)<br/>
[Админка](http://62.84.119.109/admin/)<br/>
```
Адрес электронной почты:admin@foodgram.com
Пароль: admin
```

## Описание: 

Foodgram - это сервис, который реализован для публикации рецептов. Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачать список покупок ингредиентов для добавленных в покупки рецептов.

## Как запустить проект: 

### Шаблон наполнения env-файла ( расположение файла - infra/.env ):
``` 
SECRET_KEY=default-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=login
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

### Установка
Для запуска приложения проделайте следующие шаги:


Склонируйте репозиторий:
``` 
git clone 
``` 
Перейдити в папку infra, создайте файл .env, заполните его данными из шаблона выше и запустите docker-compose.yaml (при установленном и запущенном Docker):
``` 
docker-compose up
``` 
Для пересборки контейнеров выполните команду:
``` 
docker-compose up -d --build
``` 
В контейнере backend  выполните миграции:
``` 
docker-compose exec backend  python manage.py migrate
``` 
Создатйте суперпользователя:
``` 
docker-compose exec backend python manage.py createsuperuser
``` 
Соберите статику:
``` 
docker-compose exec backend  python manage.py collectstatic --no-input
``` 
Проект запущен и доступен по адресу: localhost


### Загрузка тестовых значений в БД:


Чтобы загрузить тестовые значения в базу данных перейдите в каталог проекта и скопируйте файл базы данных в контейнер приложения:
``` 
docker cp <DATA BASE> <CONTAINER ID>:/app/<DATA BASE>
``` 
Перейдите в контейнер приложения и загрузить данные в БД:
``` 

docker container exec -it <CONTAINER ID> bash
```
```
python manage.py loaddata <DATA BASE> 
``` 

При необходимости возможно импортировать тестовые данные:
```
docker-compose exec backend python manage.py filldatabase_ing
docker-compose exec backend python manage.py filldatabase_tag
```
### Автор проекта
Шалаева Елизавета
