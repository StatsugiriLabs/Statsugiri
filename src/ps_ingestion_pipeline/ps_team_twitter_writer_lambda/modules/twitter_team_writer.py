import tweepy
import uuid
from lambda_typing.types import LambdaDict
from typing import List
from utils.base_logger import logger
from utils.constants import (
    MAX_TWEET_LENGTH,
    TWITTER_BASE_URL,
    TWITTER_DISPLAY_NAME,
    REPLAY_BASE_URL,
    SNAPSHOT_DATE_EVENT_ARG,
    FORMAT_ID_EVENT_ARG,
    TEAM_LIST_EVENT_ARG,
    PKMN_TEAM_EVENT_ARG,
    RATING_EVENT_ARG,
    ID_EVENT_ARG,
)
from utils.errors import (
    TweetExceedsLengthException,
    TwitterPostException,
    TwitterDeleteException,
)


class TwitterTeamWriter:
    def __init__(self, twitter_api_client: tweepy.API):
        self.twitter_api_client = twitter_api_client
        self.identifier = str(uuid.uuid4())

    def write(self, team_snapshot_payload: dict) -> bool:
        """
        Tweet a title thread and reply threads with the snapshot

        :param: teams_snapshot_payload
        :returns: success
        """
        tweet_ids = []
        snapshot_date = team_snapshot_payload[SNAPSHOT_DATE_EVENT_ARG]
        format_id = team_snapshot_payload[FORMAT_ID_EVENT_ARG]
        team_list = team_snapshot_payload[TEAM_LIST_EVENT_ARG]

        try:
            title_tweet_id = self.write_parent_tweet(
                self._get_title_tweet(snapshot_date, format_id)
            )
            tweet_ids.append(title_tweet_id)

            for rank, team_info in enumerate(team_list, start=1):
                team_tweet_id = self.write_child_tweet(
                    title_tweet_id, self._get_team_tweet(rank, team_info)
                )
                tweet_ids.append(team_tweet_id)
                title_tweet_id = team_tweet_id

            # Quote retweet title (ie. first) to push to top
            quote_tweet_id = self.write_quote_tweet(
                self._get_tweet_url(tweet_ids[0]), self._get_quote_tweet()
            )
            tweet_ids.append(quote_tweet_id)
            return True
        except tweepy.errors.HTTPException:
            try:
                self.delete_tweets(tweet_ids)
                raise TwitterPostException(
                    "Error writing tweets, tweets have been rolled back"
                )
            except tweepy.errors.HTTPException:
                raise TwitterDeleteException(
                    "Error deleting tweets, manual deletion required"
                )

    def write_parent_tweet(self, msg_content: str) -> int:
        """
        Post a parent-level tweet

        :param: msg_content
        :returns: tweet ID
        """
        try:
            tweet = self.twitter_api_client.update_status(msg_content)
            return tweet.id
        except tweepy.errors.HTTPException as e:
            logger.error("Unable to post parent tweet: {err}".format(err=str(e)))
            raise e

    def write_child_tweet(self, parent_id: int, msg_content: str) -> int:
        """
        Post a child tweet to a parent (eg. reply)

        :param: parent_id
        :param: msg_content
        :returns: tweet ID
        """
        try:
            tweet = self.twitter_api_client.update_status(
                status=msg_content, in_reply_to_status_id=parent_id
            )
            return tweet.id
        except tweepy.errors.HTTPException as e:
            logger.error("Unable to post child tweet: {err}".format(err=str(e)))
            raise e

    def write_quote_tweet(self, quoted_tweet_url: str, msg_content: str) -> int:
        try:
            tweet = self.twitter_api_client.update_status(
                status=msg_content, attachment_url=quoted_tweet_url
            )
            return tweet.id
        except tweepy.errors.HTTPException as e:
            logger.error("Unable to post quote tweet: {err}".format(err=str(e)))
            raise e

    def delete_tweets(self, tweet_ids: List[int] = None) -> None:
        """
        Delete tweets based on IDs provided

        :param: tweet_ids
        :returns: none
        """
        if not tweet_ids:
            logger.info("No tweets provided to delete")
        else:
            try:
                for tweet_id in tweet_ids:
                    self.twitter_api_client.destroy_status(tweet_id)
            except tweepy.errors.HTTPException as e:
                logger.error("Unable to delete tweets: {err}".format(err=str(e)))
                raise e

    def _get_tweet_url(self, tweet_id: int) -> str:
        """
        Get full tweet URL, generally for quote retweet

        :param: tweet_id
        :returns: full tweet URL
        """
        return "{twitter_base_url}/{display_name}/status/{tweet_id}".format(
            twitter_base_url=TWITTER_BASE_URL,
            display_name=TWITTER_DISPLAY_NAME,
            tweet_id=tweet_id,
        )

    def _get_title_tweet(self, snapshot_date: str, format_id: str) -> str:
        """
        Generate the title tweet for the snapshot thread

        :param: snapshot_date
        :param: format_id
        :returns: title tweet message
        """
        return "🧵 Thread for Pokémon Showdown Teams\n📅 Date: {date}\n📝 Format: {format}\n✅ Identifier: {uuid}".format(
            date=snapshot_date, format=format_id, uuid=self.identifier
        )

    def _get_team_tweet(self, rank: int, team_info: dict) -> str:
        """
        Generate the team reply tweet for the snapshot thread

        :param: rank
        :param: team_info
        :returns: team tweet message
        """
        pkmn_team = "/".join(team_info[PKMN_TEAM_EVENT_ARG])
        team_tweet = "{rank}.\n{pkmn_team}\n\n📈 Rating: {rating}\n\n📼 Replay: {replay_link}".format(
            rank=str(rank),
            pkmn_team=pkmn_team,
            rating=team_info[RATING_EVENT_ARG],
            replay_link=(REPLAY_BASE_URL + team_info[ID_EVENT_ARG]),
        )
        if len(team_tweet) > MAX_TWEET_LENGTH:
            raise TweetExceedsLengthException("Tweet exceeds maximum allotted length")
        return team_tweet

    def _get_quote_tweet(self):
        """
        Generate quote tweet to push message to top of feed

        :returns: quote tweet message
        """
        return "🐟 Order Up! 🐟\n✅ Identifier: {uuid}\n\n#OrderUpVGC".format(
            uuid=self.identifier
        )
