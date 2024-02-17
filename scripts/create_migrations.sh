#!/bin/bash -x

sleep 5

alembic upgrade head || 0

exec "$@"
