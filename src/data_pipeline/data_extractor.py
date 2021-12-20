""" Data Extractor is responsible for reading format metadata and retrieving the replay JSON """
from typing import List, Tuple
import re
import requests
from bs4 import BeautifulSoup
from constants import MAX_USERS


LADDER_BASE_URL = "https://pokemonshowdown.com/ladder/"
REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/"
REPLAY_SEARCH_BASE_URL = "https://replay.pokemonshowdown.com/search/?output=html&user="
REQUEST_TIMEOUT = 120  # [seconds]


class DataExtractor:
    """Class for ingesting, parsing, and extracting replay data"""

    def __init__(self, formats: List[str], num_teams: int = 250):
        # Initialize available formats
        self.formats = formats
        # self.replay_parser = ReplayParser()
        self.num_teams = num_teams

    def get_formats(self):
        """Return available formats"""
        return self.formats

    def get_ladder_users_and_ratings(
        self, battle_format: str, num_users: int = MAX_USERS
    ) -> List[Tuple[str, int]]:
        """Return the top users and ratings within a given format"""
        ladder_get_url = LADDER_BASE_URL + battle_format
        if battle_format not in self.formats:
            raise ValueError(f"Format ({battle_format}) is unavailable")
        if num_users > MAX_USERS:
            raise ValueError(
                f"Maximum number of users is {MAX_USERS}, {num_users} was requested"
            )

        # Retrieve ladder HTTP response content
        ladder_res = requests.get(ladder_get_url, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(ladder_res.text, "html.parser")

        # Parse for users and ratings
        users = [
            user.get_text()
            for user in soup.find_all(
                lambda predicate: predicate.name == "a"
                and "users" in predicate.get("href")
            )
        ]
        # Ratings associated with `strong` tag only
        ratings = [
            int(rating.get_text())
            for rating in soup.find_all(lambda predicate: predicate.name == "strong")
        ]

        # Combine users with ratings
        combined_users_ratings = list(zip(users, ratings))
        return combined_users_ratings[:num_users]

    def sanitize_user(self, user: str):
        """Sanitize username for non-ASCII characters and spaces"""
        user = re.sub(r"[^\x00-\x7f]", r"", user)
        user = user.replace(" ", "")
        return user

    def get_user_replay_ids(self, user: str, battle_format: str):
        """Returns a user's replays by replay ID in reverse-chronological order,
        return blank if not found"""
        sanitized_user = self.sanitize_user(user)
        user_replay_ids_get_url = REPLAY_SEARCH_BASE_URL + sanitized_user
        user_replays_res = requests.get(user_replay_ids_get_url)
        soup = BeautifulSoup(user_replays_res.text, "html.parser")

        # Parsed replays are reverse-chronological order
        replay_ids = [
            # Remove `/` character for replay ID
            replay.get("href")[1:]
            for replay in soup.find_all(
                lambda predicate: predicate.name == "a"
                and battle_format in predicate.get("href")
            )
        ]

        return replay_ids

    def get_replay_log(self, battle_format: str, replay_id: str):
        """Returns the replay log given a replay ID, blank if not found"""
        replay_log_get_url = REPLAY_BASE_URL + battle_format + "-" + replay_id + ".log"
        replay_log_res = requests.get(replay_log_get_url)
        return replay_log_res.text

    # def get_replay_parser_name(self):
    #     return self.replay_parser.get_name()

    # def set_replay_parser(self, replay_parser: ReplayParser):
    #     self.parser = replay_parser

    # def extract_info(self, battle_format: str):
    #     replay_log_res = requests.get(REPLAY_BASE_URL + "gen8vgc2021series3-1468972576" + ".log")
    #     print(replay_log_res.text)
    #     """Run data pipeline for extracting replay data"""
    #     # Retrieve top users
    #     user_ratings = self.get_ladder_users_and_ratings(battle_format, 100)

    #     # Retrieve specified number of replays
    #     teams_found = 0
    #     for user_rating in user_ratings:
    #         # Find users replays for specified format
    #         user_replay_ids = self.get_user_replay_ids(user_rating[0], battle_format)
    #         # Skip to next user if replays not found
    #         if not user_replay_ids:
    #             continue
    #         # Find replay log using most recent replay
    #         replay_log = self.get_replay_log(battle_format, user_replay_ids[0])
    #         # Skip to next user if relpay not found
    #         if not replay_log:
    #             continue
    #         # Check if there's a more elegant method
    #         teams_found += 1
    #         if teams_found == self.num_teams:
    #             break
    #         break
