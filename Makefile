# Run formatting and linting
format:
	cd formatting_scripts && ./fix_formatting.sh

# Run server
server-run:
	cd src/server && go run .

# Run data pipeline tests
drilbur-test:
	cd src/data_pipeline && PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider . -vv
