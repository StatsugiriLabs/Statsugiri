import boto3
import json
from lambda_typing.types import LambdaDict, LambdaContext
from clients.teams_ddb_client import TeamsDdbClient
from modules.ddb_teams_reader import DdbTeamsReader
from utils.base_logger import logger


TABLE_NAME = "PsIngestionTeamsTable-Beta"
GET_OPERATION = "GET"
GET_HEALTH_PATH = "/health"
GET_TEAM_PATH = "/team"


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    team_snapshot_key = "TODO"
    logger.info("Incoming request for '{key}'".format(key=team_snapshot_key))

    print(event)

    if event["httpMethod"] == GET_OPERATION and event["path"] == GET_TEAM_PATH:
        print("Receive request to get team")
    elif event["httpMethod"] == GET_OPERATION and event["path"] == GET_HEALTH_PATH:
        print("Received request for health check")
    else:
        print("Can't route...")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"success": True}),
    }
