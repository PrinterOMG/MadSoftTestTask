up-dev:
	docker compose -f docker-compose.dev.yml up --build

up-prod:
	docker compose -f docker-compose.prod.yml up --build -d

down-dev:
	docker compose -f docker-compose.dev.yml down

down-prod:
	docker compose -f docker-compose.prod.yml down

migrate-all:
	docker exec memes_api alembic upgrade heads
