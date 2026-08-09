.PHONY: install install-dev test test-cov lint format typecheck eval api ui demo-data docker-build docker-up validate clean

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install || true

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov --cov-report=term-missing --cov-report=html

lint:
	ruff check .
	black --check .

typecheck:
	mypy api analytics data_pipeline ml geo_toolkit.py

format:
	ruff check --fix .
	black .

eval:
	python -m evaluation.run_eval

validate: lint test eval

api:
	uvicorn api.main:app --reload

ui:
	streamlit run ui/streamlit_app.py

demo-data:
	python -m scripts.generate_demo_data

adk-web:
	adk web

docker-build:
	docker compose build

docker-up:
	docker compose up

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
