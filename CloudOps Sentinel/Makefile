.PHONY: install test lint run docker-build

install:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	ruff check app tests

run:
	uvicorn app.main:app --reload

docker-build:
	docker build -t cloudops-sentinel:local .

