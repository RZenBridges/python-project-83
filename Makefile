dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install
