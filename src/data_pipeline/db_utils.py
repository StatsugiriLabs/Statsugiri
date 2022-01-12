"""Database utility functions for managing tables"""
import os
from typing import List
import mypy_boto3_dynamodb as boto3_dynamodb
from constants import (
    POKEMON_TEAMS_SNAPSHOTS_TABLE_NAME,
    POKEMON_USAGE_SNAPSHOTS_TABLE_NAME,
)
from base_logger import logger

db_env_prefix = "PROD_" if os.getenv("ENV", "") == "PROD" else "DEV_"


def get_table_names(
    dynamodb_resource: boto3_dynamodb.DynamoDBServiceResource,
) -> List[str]:
    """Get all table names"""
    return [table.name for table in dynamodb_resource.tables.all()]


def create_pokemon_teams_snapshots_table(
    dynamodb_resource: boto3_dynamodb.DynamoDBServiceResource,
):
    """Creates Pokémon Teams Snapshots Table"""
    try:
        pokemon_teams_snapshots_table = dynamodb_resource.create_table(
            TableName=db_env_prefix + POKEMON_TEAMS_SNAPSHOTS_TABLE_NAME,
            KeySchema=[
                {"AttributeName": "date", "KeyType": "HASH"},
                {"AttributeName": "format_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "date", "AttributeType": "N"},
                {"AttributeName": "format_id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
            },
        )
        # Wait until table is active
        pokemon_teams_snapshots_table.meta.client.get_waiter("table_exists").wait(
            TableName=db_env_prefix + POKEMON_TEAMS_SNAPSHOTS_TABLE_NAME
        )
        logger.info("Created Pokémon Teams Snapshots Table")
    except dynamodb_resource.meta.client.exceptions.TableAlreadyExistsException as error:
        logger.error(error)
        raise error


def create_pokemon_usage_snapshots_table(
    dynamodb_resource: boto3_dynamodb.DynamoDBServiceResource,
):
    """Creates Pokémon Usage Snapshots Table"""
    try:
        pokemon_usage_snapshots_table = dynamodb_resource.create_table(
            TableName=db_env_prefix + POKEMON_USAGE_SNAPSHOTS_TABLE_NAME,
            KeySchema=[
                {"AttributeName": "date", "KeyType": "HASH"},
                {"AttributeName": "format_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "date", "AttributeType": "N"},
                {"AttributeName": "format_id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
            },
        )
        # Wait until table is active
        pokemon_usage_snapshots_table.meta.client.get_waiter("table_exists").wait(
            TableName=db_env_prefix + POKEMON_USAGE_SNAPSHOTS_TABLE_NAME
        )
        logger.info("Created Pokémon Usage Snapshots Table")
    except dynamodb_resource.meta.client.exceptions.TableAlreadyExistsException as error:
        logger.error(error)
        raise error


def write_pokemon_teams_snapshots_table(
    dynamodb_resource: boto3_dynamodb.DynamoDBServiceResource,
    pokemon_teams_snapshot_model: dict,
) -> None:
    """Write to `POKEMON_TEAMS_SNAPSHOT` table"""
    try:
        # Create table if it does not exist
        if (db_env_prefix + POKEMON_TEAMS_SNAPSHOTS_TABLE_NAME) not in get_table_names(
            dynamodb_resource
        ):
            create_pokemon_teams_snapshots_table(dynamodb_resource)

        pokemon_teams_snapshots_table = dynamodb_resource.Table(
            db_env_prefix + POKEMON_TEAMS_SNAPSHOTS_TABLE_NAME
        )
        pokemon_teams_snapshots_table.put_item(Item=pokemon_teams_snapshot_model)
    except dynamodb_resource.meta.client.exceptions.TableNotFoundException as error:
        logger.error(error)
        raise error


def write_pokemon_usage_snapshots_table(
    dynamodb_resource: boto3_dynamodb.DynamoDBServiceResource,
    pokemon_usage_snapshots_model: dict,
) -> None:
    """Write to `POKEMON_USAGE_SNAPSHOT` table"""
    try:
        # Create table if it does not exist
        if (db_env_prefix + POKEMON_USAGE_SNAPSHOTS_TABLE_NAME) not in get_table_names(
            dynamodb_resource
        ):
            create_pokemon_usage_snapshots_table(dynamodb_resource)

        pokemon_usage_snapshots_table = dynamodb_resource.Table(
            db_env_prefix + POKEMON_USAGE_SNAPSHOTS_TABLE_NAME
        )
        pokemon_usage_snapshots_table.put_item(Item=pokemon_usage_snapshots_model)
    except dynamodb_resource.meta.client.exceptions.TableNotFoundException as error:
        logger.error(error)
        raise error
