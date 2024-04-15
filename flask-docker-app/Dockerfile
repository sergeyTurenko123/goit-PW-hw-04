# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.10

# Встановимо змінну середовища
ENV APP_HOME /main

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Скопіюємо інші файли в робочу директорію контейнера
COPY "requirements.txt" "requirements.txt"
COPY "css/style.css" "css/style.css"
COPY "error.html" "error.html"
COPY "index.html" "index.html"
COPY "logo.png" "logo.png"
COPY "message.html" "message.html"
COPY "storage/data.json" "storage/data.json"
COPY "main.py" "main.py"
# Встановимо залежності всередині контейнера
RUN pip install -r requirements.txt

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 3000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "main.py"]
