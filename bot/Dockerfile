FROM python:3.11

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY --chmod=0755 entrypoint.sh /usr/local/bin/

COPY . .

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python", "src/main.py"]
