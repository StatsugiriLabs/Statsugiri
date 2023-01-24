from lambda_typing.types import LambdaDict, LambdaContext
import boto3
from clients.ps_replay_transform_client import PsReplayTransformClient
from clients.s3_replay_snapshot_reader_client import S3ReplaySnapshotReaderClient
from clients.s3_team_snapshot_writer_client import S3TeamSnapshotWriterClient
from modules.replay_parser import ReplayParser
from utils.constants import (
    REPLAYS_BUCKET_KEY_ARG,
    REPLAYS_BUCKET_NAME_ARG,
    PAYLOAD_EVENT_ARG,
    TEAMS_BUCKET_NAME,
    BUCKET_KEY_FIELD,
    BUCKET_NAME_FIELD,
)
from utils.base_logger import logger


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: team snapshot JSON
    """
    replay_snapshot_payload = event[PAYLOAD_EVENT_ARG]
    replay_snapshot_key = replay_snapshot_payload[REPLAYS_BUCKET_KEY_ARG]
    replay_snapshot_bucket_name = replay_snapshot_payload[REPLAYS_BUCKET_NAME_ARG]
    logger.info("Incoming request for '{key}".format(format=replay_snapshot_key))

    ps_replay_transform_client = PsReplayTransformClient(ReplayParser())
    s3_client = boto3.client("s3")
    s3_replay_snapshot_reader_client = S3ReplaySnapshotReaderClient(
        s3_client, replay_snapshot_bucket_name
    )
    s3_team_snapshot_writer_client = S3TeamSnapshotWriterClient(
        s3_client, TEAMS_BUCKET_NAME
    )

    replay_snapshot_dict = s3_replay_snapshot_reader_client.read(replay_snapshot_key)
    team_snapshot = ps_replay_transform_client.transform(replay_snapshot_dict)
    team_bucket_key = s3_team_snapshot_writer_client.write(team_snapshot)
    return {BUCKET_KEY_FIELD: team_bucket_key, BUCKET_NAME_FIELD: TEAMS_BUCKET_NAME}
