include .env

dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer

start:
	poetry run python3 -m page_analyzer.environment
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

new-base:
	createdb urls

drop-base:
	dropdb urls
