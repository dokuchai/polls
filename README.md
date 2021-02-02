# Polls - Опросы

Тестовое задание для собеседования в Фабрику Решений, представляющее собой проект с опросами

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
docker exec -it polls python manage.py migrate
```

При необходимости доступа к административной панели сайта выполняем:

```
docker exec -it polls python manage.py createsuperuser
```

## Запуск тестов

Запускаем тесты командой

```
docker exec -it polls pytest -p no:warnings
```

Также можем запустить тесты с проверкой покрытия кода:

```
docker exec -it polls pytest -p no:warnings --cov=.
```


