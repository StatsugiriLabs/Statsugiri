import time
from lambda_typing.types import LambdaDict, LambdaContext
from clients.ps_replay_extraction_client import PsReplayExtractionClient
from modules.replay_extractor import ReplayExtractor
from modules.ladder_retriever import LadderRetriever
from data.ps_ingest_config import PsIngestConfig
from utils.base_logger import logger
from utils.constants import (
    EVENT_FORMAT_KEY,
    VALID_FORMATS,
    NUM_USERS_TO_PULL,
)
from utils.time_utils import convert_unix_timestamp_to_str
from utils.serdes_utils import to_dict


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: replay snapshot JSON
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
        NUM_USERS_TO_PULL,
    )
    ps_replay_extraction_client = PsReplayExtractionClient(
        ReplayExtractor(LadderRetriever(), ingest_config)
    )

    replay_snapshot = ps_replay_extraction_client.process()
    return to_dict(replay_snapshot)
