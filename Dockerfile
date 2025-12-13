FROM python:3.11-slim

# Чтобы не задавал вопросы в интерактиве
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Системные пакеты (нужны для asyncpg и т.п.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Сначала зависимости — для кэша
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini


COPY pyproject.toml ./pyproject.toml
COPY README.md ./README.md

# Порт FastAPI
EXPOSE 8000

# Команда по умолчанию
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
