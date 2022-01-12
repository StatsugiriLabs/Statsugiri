""" Application-level logic for facilitating data pipeline """
import os
import json
import boto3
import botocore
from base_logger import logger
from boto3.session import Session
from lambda_typing.types import LambdaDict, LambdaContext

from data_extractor import DataExtractor
from constants import FORMATS, NUM_TEAMS, DYNAMODB_STR


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


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """Lambda handler for starting the data extraction process"""
    format_arg = event.get("format") or ""
    if not format_arg:
        raise ValueError("'format' must be provided.")

    logger.info("Initializing data pipeline...")
    session = create_session()

    data_extractor = DataExtractor(
        session.resource(DYNAMODB_STR), 1641197251, FORMATS, NUM_TEAMS
    )

    # Will run successfully if errors were not raised
    snapshots = data_extractor.extract_info(format_arg)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "pokemon_teams_snapshot_model": snapshots[
                    "pokemon_teams_snapshot_model"
                ],
                "pokemon_usage_snapshot_model": snapshots[
                    "pokemon_usage_snapshot_model"
                ],
            }
        ),
    }
