# базовый образ Python
FROM python:3.8

# Рабочая директория внутри контейнера
WORKDIR /app

# Копирование requirements.txt в контейнер
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копия всего содержимое
COPY . .

# Команда для запуска бота
CMD ["python", "main.py"]
