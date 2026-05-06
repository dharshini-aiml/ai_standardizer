.PHONY: install run test format lint docker

install:
	python -m venv .venv && .venv/bin/pip install -r requirements.txt

run:
	uvicorn app.api:app --reload

test:
	pytest

format:
	black .

lint:
	flake8 .

docker:
	docker build -t ai-standardizer:latest .
