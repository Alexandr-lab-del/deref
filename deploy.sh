#!/bin/bash

# Остановка текущего контейнера
docker-compose down

# Обновление кодовой базы
git pull origin main

# Сборка и перезапуск контейнеров
docker-compose up -d --build

# Сбор статики и миграция базы данных
docker exec -it $(docker ps -q -f "name=web") python manage.py collectstatic --noinput
docker exec -it $(docker ps -q -f "name=web") python manage.py migrate
