format:
	cd formatting_scripts && ./fix_formatting.sh

ps-ingestion-test:
	cd src/ps_ingestion_lambda && PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider . -vv

build-ps-ingestion-image:
	cd src/ps_ingestion_lambda && docker build -t ps-ingestion-lambda .
