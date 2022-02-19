# Run formatting and linting
format:
	cd formatting_scripts && ./fix_formatting.sh

# Run server
server-run:
	cd src/server && go run .

# Run server tests
server-test:
	cd src/server && go test ./tests/...

# Build server Docker image
server-docker-build:
	cd src/server && docker build -t babiri_server:latest .

# Run Docker image
server-docker-run: server-docker-build
	docker run -t -d -p 3000:3000 babiri_server:latest

# Run data pipeline tests
drilbur-test:
	cd src/data_pipeline && PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider . -vv
