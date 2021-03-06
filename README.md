# Polls - Опросы

Проект с опросами.

### Клонируем репозиторий

```
git clone https://github.com/dokuchai/polls
```

### Установка и запуск контейнеров

Из папки с репозиторием выполняем

```
docker-compose up -d --build
```

Ждем, когда произойдет билд контейнеров, после чего:

```
docker exec -it polls_app python manage.py migrate
```

При необходимости доступа к административной панели сайта выполняем:

```
docker exec -it polls_app python manage.py createsuperuser
```

## Запуск тестов

Запускаем тесты командой

```
docker exec -it polls_app pytest -p no:warnings
```

## Документация по API

Документация по API доступна по следующему URL после запуска контейнеров:

```
http://localhost:8000/swagger/
```

