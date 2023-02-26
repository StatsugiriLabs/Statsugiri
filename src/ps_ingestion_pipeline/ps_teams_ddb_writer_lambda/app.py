import boto3
from lambda_typing.types import LambdaDict, LambdaContext
from clients.teams_ddb_client import TeamsDdbClient
from clients.s3_team_snapshot_reader_client import S3TeamSnapshotReaderClient
from modules.teams_ddb_writer import DdbTeamsWriter
from utils.base_logger import logger
from utils.constants import (
    PAYLOAD_EVENT_ARG,
    TEAMS_BUCKET_KEY_ARG,
    TEAMS_BUCKET_NAME_ARG,
)

# TODO: Get table name from env var
TABLE_NAME = "PsIngestionTeamsTable-Beta"

def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    team_snapshot_payload = event[PAYLOAD_EVENT_ARG]
    team_snapshot_key = team_snapshot_payload[TEAMS_BUCKET_KEY_ARG]
    team_snapshot_bucket_name = team_snapshot_payload[TEAMS_BUCKET_NAME_ARG]
    logger.info("Incoming request for '{key}".format(key=team_snapshot_key))

    s3_client = boto3.client("s3")
    s3_team_snapshot_reader_client = S3TeamSnapshotReaderClient(
        s3_client, team_snapshot_bucket_name
    )

    ddb_client = boto3.client("dynamodb")
    teams_ddb_client = TeamsDdbClient(
        ddb_client, TABLE_NAME
    )
    ddb_teams_writer = DdbTeamsWriter(teams_ddb_client)

    team_snapshot_dict = s3_team_snapshot_reader_client.read(team_snapshot_key)
    success = ddb_teams_writer.write(team_snapshot_dict)
    return {"success": str(success)}
