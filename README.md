# Сервис авторизации

### Технологии

| Python 3.11  | FastAPI   | SQLAlchemy     |
|--------------|-----------|----------------|
| **Pydantic** | **Redis** | **PostgreSQL** |

### Запуск проекта

1. Создать виртуальное окружение: `python -m venv venv`

2. Активировать виртуальное окружение: `source ./venv/bin/activate`

3. Установить пакет: `pip install -e .`

4. Применить миграции: `python -m alembic upgrade head`

5. Запустить проект: `python -m uvicorn auth.main:app --reload`

6. Если необходима установка дополнительных пакетов: `pip install -e .[dev]`
