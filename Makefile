.PHONY: install dev test lint run frontend docker-up docker-down

install:
	pip install -r backend/requirements-dev.txt

dev: install
	cd frontend && npm install

test:
	pytest backend/tests

lint:
	ruff check backend/

run:
	uvicorn backend.app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
