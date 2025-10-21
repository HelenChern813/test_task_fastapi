# (1) Базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Определяем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
