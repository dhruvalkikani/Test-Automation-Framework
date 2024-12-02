 # Install dependencies
install:
	poetry install

# Run linting
lint:
	poetry run flake8 tests/

# Run tests
test:
	poetry run pytest tests/

# Run Playwright install to set up browsers
playwright-install:
	poetry run playwright install
