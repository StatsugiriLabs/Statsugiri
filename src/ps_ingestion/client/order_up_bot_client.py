import tweepy
import uuid
from data.team_snapshot_info import TeamSnapshotInfo
from typing import List
from utils.constants import REPLAY_BASE_URL, TWITTER_DISPLAY_NAME
from utils.base_logger import logger

MAX_TWEET_LENGTH = 280
TWITTER_BASE_URL = "https://twitter.com"


class OrderUpBotClient:
    def __init__(self, api_client: tweepy.API, format_id: str):
        self.api_client = api_client
        self.format_id = format_id

    """
    Tweet a title thread and reply threads with the snapshot

    :param: teams_snapshot
    :param: snapshot_date
    :returns: None
    """

    def tweet(self, teams_snapshot: List[TeamSnapshotInfo], snapshot_date: str) -> None:
        tweet_ids = []
        try:
            parent_tweet_status = self.api_client.update_status(
                self._get_title_tweet(snapshot_date)
            )
            parent_tweet_id = parent_tweet_status.id
            tweet_ids.append(parent_tweet_id)

            quote_tweet_url = (
                "{twitter_base_url}/{display_name}/status/{tweet_id}".format(
                    twitter_base_url=TWITTER_BASE_URL,
                    display_name=TWITTER_DISPLAY_NAME,
                    tweet_id=parent_tweet_id,
                )
            )

            for index, team in enumerate(teams_snapshot):
                rank = index + 1
                child_tweet_msg = self._get_team_tweet(rank, team)
                if len(child_tweet_msg) > MAX_TWEET_LENGTH:
                    logger.warning(
                        "Tweet cannot exceed {max_length} characters, posting shortened version".format(
                            max_length=str(MAX_TWEET_LENGTH)
                        )
                    )
                    child_tweet_msg = self._get_error_tweet(rank)
                child_tweet_status = self.api_client.update_status(
                    status=child_tweet_msg, in_reply_to_status_id=parent_tweet_id
                )
                tweet_ids.append(child_tweet_status.id)
                parent_tweet_id = child_tweet_status.id

            # Quote retweet to push to top of feed
            quote_tweet_status = self.api_client.update_status(
                status=self._get_quote_tweet(), attachment_url=quote_tweet_url
            )
            tweet_ids.append(quote_tweet_status.id)
        except tweepy.errors.HTTPException as post_e:
            logger.error("Internal Twitter error, rolling back tweets")
            try:
                for tweet_id in tweet_ids:
                    self.api_client.destroy_status(tweet_id)
            except tweepy.errors.HTTPException as delete_e:
                logger.error("Unable to delete tweets, manual deletion required")
                raise delete_e
            raise post_e

    """
    Generate the title tweet for the snapshot thread

    :param: snapshot_date
    :returns: title tweet message
    """

    def _get_title_tweet(self, snapshot_date: str) -> str:
        return "🧵 Thread for Pokémon Showdown Teams\n📅 Date: {date}\n📝 Format: {format}\n✅ Identifier: {uuid}".format(
            date=snapshot_date, format=self.format_id, uuid=str(uuid.uuid4())
        )

    """
    Generate the team reply tweet for the snapshot thread

    :param: rank
    :param: team
    :returns: child tweet message
    """

    def _get_team_tweet(self, rank: int, team: TeamSnapshotInfo) -> str:
        pkmn_team = "/".join(team.pkmn_team)
        team_tweet = "{rank}.\n{pkmn_team}\n\n📈 Rating: {rating}\n\n📼 Replay: {replay_link}".format(
            rank=str(rank),
            pkmn_team=pkmn_team,
            rating=team.rating,
            replay_link=(REPLAY_BASE_URL + team.id),
        )
        return team_tweet

    """
    Generate error tweet, generally when tweet exceeds MAX_TWEET_LENGTH

    :param: rank
    :returns: error tweet message
    """

    def _get_error_tweet(self, rank: int) -> str:
        return "{rank}.\n⚠️ Twitter client error, skipping...".format(rank=str(rank))

    """
    Generate quote tweet to push message to top of feed

    :returns: quote tweet message
    """

    def _get_quote_tweet(self):
        return "🐟 Order Up! 🐟\n✅ Identifier: {uuid}\n\n#OrderUpVGC".format(
            uuid=str(uuid.uuid4())
        )
