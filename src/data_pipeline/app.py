""" Application-level logic for facilitating data pipeline """
from base_logger import logger

from data_extractor import DataExtractor
from constants import FORMATS


def main():
    """Main function"""
    logger.info("Initializing data pipeline...")
    data_extractor = DataExtractor(FORMATS)
    data_extractor.extract_info("gen8vgc2021series11")


if __name__ == "__main__":
    main()
