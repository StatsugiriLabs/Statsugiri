import boto3
from lambda_typing.types import LambdaDict, LambdaContext
from clients.teams_ddb_client import TeamsDdbClient
from modules.teams_ddb_reader import DdbTeamsWriter
from utils.base_logger import logger

# from utils.constants import (
# )

TABLE_NAME = "PsIngestionTeamsTable-Prod"


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    team_snapshot_key = "TODO"
    logger.info("Incoming request for '{key}".format(key=team_snapshot_key))

    # if event.routeKey == "GET /teams":
    #     print("Receive request to get all teams")
    # elif event.routeKey == "GET /teams/{id}":
    #     print("Receive request to get team with ID: " + str(id))

    return {"success": "true"}
