#!/bin/bash -x

sleep 5

alembic upgrade head || 0

python src/main.py || 0

exec "$@"
