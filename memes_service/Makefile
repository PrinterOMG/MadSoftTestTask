make-migrations:
	docker exec memes_api alembic revision --autogenerate -m "$(message)"

migrate:
	docker exec memes_api alembic upgrade heads

run-test:
	poetry run pytest -vv tests
