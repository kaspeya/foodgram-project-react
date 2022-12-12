![example event parameter](https://github.com/kaspeya/foodgram-project-react/actions/workflowsfoodgram-project-react.yml/badge.svg?event=push)
# FoodGram ( docker-compose )

#### Проект доступен по следующим ссылкам:

[Админка](http://130.193.36.243/admin/)<br/>
[API](http://130.193.36.243/api/v1)<br/>
Документация в формате [ReDoc](http://130.193.36.243/redoc)<br/>

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
В контейнере web выполните миграции:
``` 
docker-compose exec web python manage.py migrate
``` 
Создатйте суперпользователя:
``` 
docker-compose exec web python manage.py createsuperuser
``` 
Соберите статику:
``` 
docker-compose exec web python manage.py collectstatic --no-input
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
