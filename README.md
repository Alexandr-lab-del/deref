## Установка и запуск

1. Скачайте репозиторий проекта.

2. Убедитесь, что на вашем компьютере установлен Docker и Docker Compose.

3. Создайте файл `.env` на основе `.env.example`

4. Заполните все переменные окружения в .env.
5. Соберите и запустите проект:
   docker-compose up --build
6. Проект будет доступен по адресу http://localhost:8000.
7. Проверка сервисов
* Django: Приложение доступно по порту 8000 (например, http://localhost:8000).
* PostgreSQL: База данных работает на порту 5432. Вы можете подключиться к ней с помощью любого клиента, используя данные из .env.
* Redis: Redis доступен на порту 6379.
* Celery worker: Работает в фоновом режиме, обрабатывает задачи из очередей.
* Celery beat: Автоматически запускает периодические задачи.
8. Основные команды
* Запустить проект:    docker-compose up --build
* Остановить проект:    docker-compose down
* Позволяет просматривать логи всех контейнеров: docker-compose logs
* Выводит список всех контейнеров: docker-compose ps
* Очистить контейнеры и данные:    docker-compose down -v
* Запустить миграции вручную:    docker-compose exec web python manage.py migrate
