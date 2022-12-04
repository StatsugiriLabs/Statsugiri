"""Database utility functions for managing tables"""
from typing import List

import pymongo
from utils.env_configs import MONGOURI
from utils.constants import (
    POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME,
    POKEMON_USAGE_SNAPSHOTS_COLLECTION_NAME,
    DB_CLUSTER_NAME,
)
from utils.base_logger import logger


def create_pymongo_client() -> pymongo.MongoClient:
    """Create pymongo client"""
    mongo_conn_str = MONGOURI
    if not mongo_conn_str:
        raise ValueError(
            "Please set your MongoDB Atlas connection URI as env var, 'MONGOURI'"
        )

    client = pymongo.MongoClient(mongo_conn_str)
    if client is None:
        raise ConnectionError("Could not connect to MongoDB")

    return client


def get_collection_names(
    mongo_client: pymongo.MongoClient,
) -> List[str]:
    """Get all collection names"""
    try:
        database = mongo_client[DB_CLUSTER_NAME]
        return database.list_collection_names()

    except pymongo.errors.OperationFailure as error:
        logger.error(error)
        raise error


def create_pokemon_teams_snapshots_collection(
    mongo_client: pymongo.MongoClient,
) -> pymongo.database.Database:
    """Creates Pokémon Teams Snapshots collection"""
    try:
        collection_name = POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME
        collection = mongo_client[collection_name]
        logger.info("Created Pokémon Teams Snapshots Table")
        return collection

    except pymongo.errors.WriteError as error:
        logger.error(error)
        raise error
    except pymongo.errors.ServerSelectionTimeoutError as error:
        logger.error(error)
        raise error


def create_pokemon_usage_snapshots_collection(
    mongo_client: pymongo.MongoClient,
) -> pymongo.database.Database:
    """Creates Pokémon Usage Snapshots collection"""
    try:
        database = mongo_client[DB_CLUSTER_NAME]
        collection = database[POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME]
        logger.info("Created Pokémon Usage Snapshots Table")
        return collection

    except pymongo.errors.WriteError as error:
        logger.error(error)
        raise error
    except pymongo.errors.ServerSelectionTimeoutError as error:
        logger.error(error)
        raise error


def write_pokemon_teams_snapshots_collection(
    mongo_client: pymongo.MongoClient,
    pokemon_teams_snapshot_model: dict,
) -> pymongo.results.InsertOneResult:
    """Write to `POKEMON_TEAMS_SNAPSHOT` collection"""
    try:
        # Create table if it does not exist
        if (POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME) not in get_collection_names(
            mongo_client
        ):
            create_pokemon_teams_snapshots_collection(mongo_client)

        database = mongo_client[DB_CLUSTER_NAME]
        collection = database[POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME]
        inserted_res = collection.insert_one(pokemon_teams_snapshot_model)
        logger.info("Wrote to POKEMON_TEAMS_SNAPSHOT collection")
        return inserted_res

    except pymongo.errors.WriteError as error:
        logger.error(error)
        raise error
    except pymongo.errors.ServerSelectionTimeoutError as error:
        logger.error(error)
        raise error


def write_pokemon_usage_snapshots_collection(
    mongo_client: pymongo.MongoClient,
    pokemon_usage_snapshots_model: dict,
) -> pymongo.results.InsertOneResult:
    """Write to `POKEMON_USAGE_SNAPSHOT` collection"""
    try:
        # Create collection if it does not exist
        if (POKEMON_USAGE_SNAPSHOTS_COLLECTION_NAME) not in get_collection_names(
            mongo_client
        ):
            create_pokemon_usage_snapshots_collection(mongo_client)

        database = mongo_client[DB_CLUSTER_NAME]
        collection = database[POKEMON_USAGE_SNAPSHOTS_COLLECTION_NAME]
        inserted_res = collection.insert_one(pokemon_usage_snapshots_model)
        logger.info("Wrote to POKEMON_USAGE_SNAPSHOT collection")
        return inserted_res

    except pymongo.errors.WriteError as error:
        logger.error(error)
        raise error
    except pymongo.errors.ServerSelectionTimeoutError as error:
        logger.error(error)
        raise error
