import time
import boto3
from lambda_typing.types import LambdaDict, LambdaContext
from clients.ps_replay_extraction_client import PsReplayExtractionClient
from clients.s3_replay_snapshot_writer_client import S3ReplaySnapshotWriterClient
from modules.replay_extractor import ReplayExtractor
from modules.ladder_retriever import LadderRetriever
from data.ps_ingest_config import PsIngestConfig
from utils.base_logger import logger
from utils.constants import (
    EVENT_FORMAT_KEY,
    VALID_FORMATS,
    NUM_USERS_TO_PULL,
    BUCKET_KEY_FIELD,
    BUCKET_NAME_FIELD,
    REPLAYS_BUCKET_NAME,
)
from utils.time_utils import convert_unix_timestamp_to_str


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: S3 replay bucket key for snapshot
    """
    format_to_search = event.get(EVENT_FORMAT_KEY) or ""
    logger.info("Incoming request for '{format}".format(format=format_to_search))

    # Request validation
    if not format_to_search:
        raise ValueError(
            "'{format_key}' key must be provided or an accepted format.".format(
                format_key=EVENT_FORMAT_KEY
            )
        )

    if format_to_search not in VALID_FORMATS:
        raise ValueError(
            "'{format}' is not accepted, please try a different format.".format(
                format=format_to_search
            )
        )

    ingest_config = PsIngestConfig(
        convert_unix_timestamp_to_str(int(time.time())),
        format_to_search,
        int(NUM_USERS_TO_PULL),
    )
    ps_replay_extraction_client = PsReplayExtractionClient(
        ReplayExtractor(LadderRetriever(), ingest_config)
    )
    s3_client = boto3.client("s3")
    s3_replay_snapshot_writer_client = S3ReplaySnapshotWriterClient(
        s3_client, REPLAYS_BUCKET_NAME
    )

    replay_snapshot = ps_replay_extraction_client.process()
    bucket_key = s3_replay_snapshot_writer_client.write(replay_snapshot)
    return {BUCKET_KEY_FIELD: bucket_key, BUCKET_NAME_FIELD: REPLAYS_BUCKET_NAME}
