poetry_install_dev:
	poetry install --with dev,test

poetry_install:
	poetry install

build:
	docker compose build

up:
	docker compose up -d

up_build:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

migrate_db:
	alembic upgrade head

dev:
	@export MYSQL_HOST=localhost
	@export MYSQL_PORT=3307
	@echo "Starting MySQL container..."
	@docker compose up -d --build auth-db
	@echo "Waiting for MySQL to be ready..."
	@sleep 15
	@echo "Applying migrations..."
	@./src/config/init_db/init_db.sh
	@echo "Starting Uvicorn..."
	@trap 'docker compose down --remove-orphans' INT TERM EXIT; \
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8005

test_watch:
	ENV=test poetry run ptw --runner 'pytest --ff $(extra)'

test_parallel:
	ENV=test pytest --cov=src --numprocesses auto --dist loadfile --max-worker-restart 0 $(extra)

test_last_failed:
	ENV=test poetry run ptw --runner 'pytest --ff --lf $(extra)'

test_coverage:
	coverage report --include="src/*" --omit="*/dependency_injector/*,tests/*"

coverage_xml:
	coverage xml --include="src/*" --omit="*/dependency_injector/*,tests/*"
