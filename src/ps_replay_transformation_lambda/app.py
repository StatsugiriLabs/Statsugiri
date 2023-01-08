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
from data.ingest_data_info import IngestDataInfo
from utils.time_utils import convert_unix_timestamp_to_str


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: HTTP response
    """
    return "test works"


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
