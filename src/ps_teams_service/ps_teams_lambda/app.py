import boto3
from lambda_typing.types import LambdaDict, LambdaContext
from utils.base_logger import logger

# from utils.constants import (
# )


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    team_snapshot_key = "TODO"
    logger.info("Incoming request for '{key}".format(key=team_snapshot_key))
    # ddb_client = boto3.client("dynamodb")

    if event.routeKey == "GET /teams":
        print("Receive request to get all teams")
    elif event.routeKey == "GET /items/{id}":
        print("Receive request to get team with ID: " + str(id))

    return {"success": "true"}
