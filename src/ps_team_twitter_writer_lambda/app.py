import tweepy
from lambda_typing.types import LambdaDict, LambdaContext
from clients.ps_team_twitter_writer_client import PsTeamTwitterWriterClient
from modules.twitter_team_writer import TwitterTeamWriter
from utils.base_logger import logger
from utils.constants import (
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    FORMAT_ID_EVENT_ARG,
    PAYLOAD_EVENT_ARG
)


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    team_snapshot_payload = event[PAYLOAD_EVENT_ARG]
    team_snapshot_format = team_snapshot_payload[FORMAT_ID_EVENT_ARG]
    logger.info("Incoming request for '{format}".format(format=team_snapshot_format))

    ps_team_twitter_writer_client = PsTeamTwitterWriterClient(
        TwitterTeamWriter(init_twitter_api_client())
    )

    success = ps_team_twitter_writer_client.write(team_snapshot_payload)
    return {"success": str(success)}


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
        raise
