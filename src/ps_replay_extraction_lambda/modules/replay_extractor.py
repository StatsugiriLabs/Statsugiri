import requests
from typing import List
from utils.base_logger import logger
from data.replay_info import ReplayInfo
from data.ps_ingest_config import PsIngestConfig
from data.ladder_user_info import LadderUserInfo
from data.replay_snapshot import ReplaySnapshot
from modules.ladder_retriever import LadderRetriever
from utils.request_utils import get_soup_from_url, get_response_from_url
from utils.time_utils import convert_unix_timestamp_to_str
from utils.constants import REPLAY_BASE_URL
from utils.errors import LadderNotFoundException, ReplayJsonRetrievalException

REPLAY_SEARCH_BASE_URL = (
    "https://replay.pokemonshowdown.com/search/?output=html&page=1&user="
)


class ReplayExtractor:
    def __init__(
        self, ladder_retriever: LadderRetriever, ps_ingest_config: PsIngestConfig
    ):
        self.ladder_retriever = ladder_retriever
        self.ingest_config = ps_ingest_config

    def get_replay_snapshot(self) -> List[ReplayInfo]:
        """
        Retrieve replay snapshot for the date

        :returns: replay snapshot
        """
        format_id = self.ingest_config.format_id

        top_ladder_users = self.ladder_retriever.get_users(format_id)
        if not top_ladder_users:
            logger.warning("Could not retrieve ladder rankings, aborting...")
            raise LadderNotFoundException(
                "Could not retrieve ladder rankings for {format}".format(
                    format=format_id
                )
            )

        replays = self._get_ladder_replays(top_ladder_users)
        return ReplaySnapshot(self.ingest_config.snapshot_date, format_id, replays)

    def _get_most_recent_replay_id(self, username: str) -> str:
        """
        Retrieve user's most recent format replay ID

        :param: username Username to search replays for
        :returns: ID of most recent format replay, empty string if Exception
        """
        replay_search_url = REPLAY_SEARCH_BASE_URL + username
        try:
            replay_search_soup = get_soup_from_url(replay_search_url)
            # Assume replays are sorted reverse-chronologically
            replay_id = [
                # Remove `/` character for replay ID
                # eg. <a href="/gen8vgc2020-1197324298" data-target="push"><small>...
                replay.get("href")[1:]
                for replay in replay_search_soup.find_all(
                    lambda predicate: predicate.name == "a"
                    and self.ingest_config.format_id in predicate.get("href")
                )
            ]
            return replay_id[0] if replay_id else ""
        except Exception as e:
            logger.warning(
                "Unable to reach server for replays: {err}".format(err=str(e))
            )
            return ""

    def _get_ladder_replays(self, ladder_users: List[LadderUserInfo]):
        """
        Retrieve public ladder replays from the ladder users

        :param: ladder_users
        :returns: list of replays
        """
        replay_list = []
        teams_found = 0

        for user_info in ladder_users:
            most_recent_replay_id = self._get_most_recent_replay_id(user_info.username)
            if not most_recent_replay_id:
                logger.info(
                    "No '{format}' replays found for {username}, continuing to next".format(
                        format=self.ingest_config.format_id, username=user_info.username
                    )
                )
            else:
                logger.info(
                    "Found '{format}' replay for {username}".format(
                        format=self.ingest_config.format_id, username=user_info.username
                    )
                )
                replay_info = self._get_replay_info(user_info, most_recent_replay_id)
                replay_list.append(replay_info)
                teams_found += 1
                if teams_found == self.ingest_config.num_replays_to_pull:
                    break
        return replay_list

    def _get_replay_info(self, user_info: LadderUserInfo, replay_id: str) -> ReplayInfo:
        """
        Transforming user info and replay ID to ReplayInfo

        :param: user_info
        :param: replay_id
        :returns: ReplayInfo if successful, placeholder ReplayInfo if exception
        """
        try:
            replay_json = self._get_replay_json_from_id(replay_id)
            replay_info = ReplayInfo(
                replay_json["id"],
                user_info.username,
                user_info.rating,
                self.ingest_config.format_id,
                replay_json["log"],
                convert_unix_timestamp_to_str(replay_json["uploadtime"]),
            )
            return replay_info
        except Exception as e:
            logger.warning("Unable to retrieve replay: {err}".format(err=str(e)))
            return ReplayInfo(
                "unknown_id",
                user_info.username,
                user_info.rating,
                self.ingest_config.format_id,
                "unknown_log",
                "1970-01-01",
            )

    def _get_replay_json_from_id(self, replay_id: str) -> dict:
        """
        Retrieve replay JSON from PS servers given an ID

        :param: replay_id
        :returns: replay metadata JSON
        """
        try:
            replay_data_get_url = REPLAY_BASE_URL + replay_id + ".json"
            replay_data_res = get_response_from_url(replay_data_get_url)
            return {} if not replay_data_res else replay_data_res.json()
        except Exception as e:
            logger.error("Unable to retrieve replay JSON: {err}".format(err=str(e)))
            raise ReplayJsonRetrievalException(
                "Error retrieving replay JSON for '{replay_id}'".format(
                    replay_id=replay_id
                )
            )
