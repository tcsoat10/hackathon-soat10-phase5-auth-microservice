#!/bin/sh
set -e

echo "Application is ready to start..." 

MAX_RETRIES=3000
COUNT=0

echo "MYSQL_HOST: $MYSQL_HOST"
echo "MYSQL_PORT: $MYSQL_PORT"

while ! nc -zv $MYSQL_HOST $MYSQL_PORT; do
  sleep 2
  COUNT=$((COUNT+1))
  if [ $COUNT -ge $MAX_RETRIES ]; then
    echo "Database is not ready after $MAX_RETRIES attempts, exiting..."
    exit 1
  fi
done

echo "Database is up, applying migrations..."
poetry run alembic upgrade head
