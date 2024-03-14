SRC_DIR = ./src/

.PHONY: check fix run

check:
	poetry run black --version
	poetry run black --check --line-length=100 $(SRC_DIR)
	poetry run isort --version
	poetry run isort --check-only $(SRC_DIR)
	poetry run ruff --version
	poetry run ruff check $(SRC_DIR)

fix:
	poetry run black --line-length=100 $(SRC_DIR)
	poetry run isort $(SRC_DIR)
	poetry run ruff check --fix $(SRC_DIR)

run:
	poetry run uvicorn src.main:app --reload --reload-exclude tests --port $${BACKEND_PORT:-8080} --host host.docker.internal