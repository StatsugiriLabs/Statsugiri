# Run formatting and linting
format:
	cd formatting_scripts && ./fix_formatting.sh

# Run data pipeline tests
drilbur-test:
	cd src/data_ingestion && PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider . -vv
