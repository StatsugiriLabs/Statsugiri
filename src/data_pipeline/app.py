""" Application-level logic for facilitating data pipeline """
import logging

# from data_extractor import DataExtractor
from constants import FORMATS


def init_logging(level: int):
    """Initialize logging configurations"""
    logging.basicConfig(level=level)


def main():
    """Main function"""
    init_logging(logging.INFO)
    logging.info("Initializing data pipeline...")
    # data_extractor = DataExtractor(FORMATS)
    # data_extractor.extract_info("gen8vgc2021series11")


if __name__ == "__main__":
    main()
