import json
import time
import tweepy
from lambda_typing.types import LambdaDict, LambdaContext
from client.ps_ingestion_client import PsIngestionClient
from client.order_up_bot_client import OrderUpBotClient
from modules.replay_handler import ReplayHandler
from modules.replay_parser import ReplayParser
from modules.ladder_retriever import LadderRetriever
from utils.base_logger import logger
from utils.constants import (
    EVENT_FORMAT_KEY,
    CURR_VGC_FORMAT,
    VALID_FORMATS,
    NUM_USERS_TO_PULL,
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
)
from data.ingest_data_info import IngestDataInfo
from utils.time_utils import convert_unix_timestamp_to_str


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: HTTP response
    """
    format_to_search = event.get(EVENT_FORMAT_KEY) or ""
    if not format_to_search or format_to_search not in VALID_FORMATS:
        # Handle bad request
        logger.warning(
            "'{format_key}' key must be provided or an accepted format.".format(
                format_key=EVENT_FORMAT_KEY
            )
        )

        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "Error": "'{format_key}' key must be provided or an accepted format.".format(
                        format_key=EVENT_FORMAT_KEY
                    )
                }
            ),
        }

    # Initialize clients
    order_up_bot_client = OrderUpBotClient(init_twitter_api_client(), format_to_search)
    ingestion_client = PsIngestionClient(
        ReplayHandler(format_to_search, LadderRetriever()),
        ReplayParser(),
    )
    # Initialize ingestion metadata
    curr_ingest_info = IngestDataInfo(
        convert_unix_timestamp_to_str(int(time.time())), NUM_USERS_TO_PULL
    )
    teams_snapshot = ingestion_client.process(curr_ingest_info)

    # OrderUpTeamsBot currently only supports VGC to mitigate Twitter rate-limiting
    if format_to_search == CURR_VGC_FORMAT:
        order_up_bot_client.tweet(teams_snapshot, curr_ingest_info.snapshot_date)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"Format": format_to_search}),
    }


def init_twitter_api_client() -> tweepy.API:
    """
    Initialize the Twitter API client
    :returns: Authorized Tweepy API client
    """
    try:
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweepy.API(auth)
    except tweepy.errors.HTTPException as e:
        logger.error("Unable to authenticate Twitter client")
        raise e
