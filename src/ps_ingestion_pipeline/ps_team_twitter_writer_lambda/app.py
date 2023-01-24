import tweepy
import boto3
from lambda_typing.types import LambdaDict, LambdaContext
from clients.ps_team_twitter_writer_client import PsTeamTwitterWriterClient
from clients.s3_team_snapshot_reader_client import S3TeamSnapshotReaderClient
from modules.twitter_team_writer import TwitterTeamWriter
from utils.base_logger import logger
from utils.constants import (
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    PAYLOAD_EVENT_ARG,
    TEAMS_BUCKET_KEY_ARG,
    TEAMS_BUCKET_NAME_ARG,
)


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    team_snapshot_payload = event[PAYLOAD_EVENT_ARG]
    team_snapshot_key = team_snapshot_payload[TEAMS_BUCKET_KEY_ARG]
    team_snapshot_bucket_name = team_snapshot_payload[TEAMS_BUCKET_NAME_ARG]
    logger.info("Incoming request for '{key}".format(format=team_snapshot_key))

    ps_team_twitter_writer_client = PsTeamTwitterWriterClient(
        TwitterTeamWriter(init_twitter_api_client())
    )
    s3_client = boto3.client("s3")
    s3_team_snapshot_reader_client = S3TeamSnapshotReaderClient(
        s3_client, team_snapshot_bucket_name
    )

    team_snapshot_dict = s3_team_snapshot_reader_client.read(team_snapshot_key)
    success = ps_team_twitter_writer_client.write(team_snapshot_dict)
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
