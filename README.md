## Общая настройка

```bash
# создание единой docker-сети
docker network create booknet
```

### PostgreSQL и Redis (Linux)

```bash
# контейнер для PosgreSQL 17
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=booknet \
    --volume pg_booking_db_data:/var/lib/postgresql/data \
    -d postgres:17


# контейнер Redis
docker run --name booking_redis \
    -p 7379:6379 \
    --network=booknet \
    -d redis
```

### PostgreSQL и Redis (Windows)

```bash
# контейнер для PosgreSQL 17
docker run --name booking_db ^
    -p 6432:5432 ^
    -e POSTGRES_USER=abcde ^
    -e POSTGRES_PASSWORD=abcde ^
    -e POSTGRES_DB=booking ^
    --network=booknet ^
    --volume pg_booking_db_data:/var/lib/postgresql/data ^
    -d postgres:17


# контейнер Redis
docker run --name booking_redis ^
    -p 7379:6379 ^
    --network=booknet ^
    -d redis
```

## Запуск с помощью Dockerfile

```bash
# создание docker-образа приложения
docker build -t booking_app_image .
```

### Запуск контейнеров (Linux)

```bash
# контейнер для FastAPI
docker run --name booking_backend \
    -p 8888:8000 \
    --network=booknet \
    --volume ./src/media/images:/app/src/media/images \
    -d booking_app_image


# контейнер celery worker
docker run --name booking_celery_worker \
    --network=booknet \
    --volume ./src/media/images:/app/src/media/images \
    booking_app_image \
    poetry run celery --app=src.tasks.app:celery_app worker -l INFO

# контейнер celery worker beat
docker run --name booking_celery_beat \
    --network=booknet \
    booking_app_image \
    poetry run celery --app=src.tasks.app:celery_app beat -l INFO
```

### Запуск контейнеров (Windows)

```bash
# контейнер для FastAPI
docker run --name booking_backend ^
    -p 8888:8000 ^
    --network=booknet ^
    --volume ./src/media/images:/app/src/media/images ^
    -d booking_app_image


# контейнер celery worker
docker run --name booking_celery_worker ^
    --network=booknet ^
    --volume ./src/media/images:/app/src/media/images ^
    booking_app_image ^
    poetry run celery --app=src.tasks.app:celery_app worker -l INFO


# контейнер celery beat
docker run --name booking_celery_beat ^
    --network=booknet ^
    booking_app_image ^
    poetry run celery --app=src.tasks.app:celery_app beat -l INFO
```


## Запуск с помощью  Docker-compose

```bash
# собрать все контейнеры
docker compose build

# запустить все контейнеры
docker compose up
```
