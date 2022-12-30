# Run formatting and linting
format:
	cd formatting_scripts && ./fix_formatting.sh

# Run PS ingestion tests
ps-ingestion-test:
	cd src/ps_ingestion && PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider . -vv
