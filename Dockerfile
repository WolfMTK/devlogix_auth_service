FROM python:3.11-alpine AS base

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

RUN pip install gunicorn --no-cache-dir

FROM base AS build

COPY src src
COPY alembic.ini alembic.ini
COPY pyproject.toml pyproject.toml

RUN pip install -e .

COPY --chmod=0755 scripts/create_migrations.sh /usr/local/bin

ENTRYPOINT ["usr/local/bin/create_migrations.sh"]

FROM build AS run

CMD gunicorn auth.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000