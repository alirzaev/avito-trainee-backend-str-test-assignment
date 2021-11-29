# Решение тестового задания для backend-разработчиков от avito.ru

Решение [тестового задания](https://github.com/avito-tech/verticals/blob/master/trainee/backend-str.md) для backend-разработчиков от [avito](https://avito.ru/)

## Project setup

### Development

```shell script
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

### Docker

```shell script
docker-compose up
```

## API documentation

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Unit tests

```shell script
pytest
```