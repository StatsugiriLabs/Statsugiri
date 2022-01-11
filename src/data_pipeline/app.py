""" Application-level logic for facilitating data pipeline """
import os
import boto3
import botocore
from base_logger import logger
from boto3.session import Session

from data_extractor import DataExtractor
from constants import FORMATS, NUM_TEAMS, DYNAMODB_STR

DYNAMODB_STR = "dynamodb"


def create_session() -> Session:
    """Create a session with AWS credentials"""
    try:
        # Define environment variables by running `export X=Y`
        access_key_id = os.environ["ACCESS_KEY_ID"]
        secret_access_key = os.environ["SECRET_ACCESS_KEY"]
        region_name = os.environ["REGION_NAME"]
        if not access_key_id or not secret_access_key or not region_name:
            raise ValueError(
                "Please assign values to environment variables for \
                ACCESS_KEY_ID, SECRET_ACCESS_KEY, and REGION_NAME"
            )

        return boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )
    except botocore.exceptions.NoCredentialsError as error:
        logger.error(error)
        raise error
    except botocore.exceptions.PartialCredentialsError as error:
        logger.error(error)
        raise error


def main():
    """Main function"""
    logger.info("Initializing data pipeline...")
    session = create_session()
    data_extractor = DataExtractor(
        session.resource(DYNAMODB_STR), 1641197251, FORMATS, NUM_TEAMS
    )
    data_extractor.extract_info("gen8vgc2021series11")


if __name__ == "__main__":
    main()
