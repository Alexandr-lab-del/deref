# Используем официальный Python-образ
FROM python:3.10-slim
RUN python -m pip install --upgrade pip
# Настройки рабочего каталога
WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev && apt-get clean

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта в контейнер
COPY . .

# Открытие порта приложения
EXPOSE 8000

# Запуск серверного приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
