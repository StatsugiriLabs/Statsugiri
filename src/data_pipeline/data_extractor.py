""" Data Extractor is responsible for reading format metadata and retrieving the replay JSON """
from typing import List, Tuple
from base_logger import logger
import re
import requests
from bs4 import BeautifulSoup
from constants import MAX_USERS
from log_handler import LogHandler


LADDER_BASE_URL = "https://pokemonshowdown.com/ladder/"
REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/"
REPLAY_SEARCH_BASE_URL = "https://replay.pokemonshowdown.com/search/?output=html&user="
REQUEST_TIMEOUT = 120  # [seconds]


class DataExtractor:
    """Class for ingesting, parsing, and extracting replay data"""

    def __init__(self, formats: List[str], num_teams: int = 250):
        # Initialize available formats
        self.formats = formats
        self.num_teams = num_teams
        self.log_handler = LogHandler()

    def get_formats(self):
        """Return available formats"""
        return self.formats

    def get_ladder_users_and_ratings(
        self, format_id: str, num_users: int = MAX_USERS
    ) -> List[Tuple[str, int]]:
        """Return the top users and ratings within a given format"""
        ladder_get_url = LADDER_BASE_URL + format_id
        if format_id not in self.formats:
            raise ValueError(f"Format ({format_id}) is unavailable")
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

    def get_user_replay_ids(self, user: str, format_id: str):
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
                and format_id in predicate.get("href")
            )
        ]

        return replay_ids

    def get_replay_data(self, replay_id: str):
        """Returns the replay data JSON given a replay ID, blank if not found"""
        replay_data_get_url = REPLAY_BASE_URL + replay_id + ".json"
        replay_data_res = requests.get(replay_data_get_url)
        return {} if not replay_data_res else replay_data_res.json()


    def extract_info(self, format_id: str):
        """Run data pipeline for extracting replay data"""
        # Retrieve top users
        logger.info("Retrieving top users...")
        user_ratings = self.get_ladder_users_and_ratings(format_id, 25)

        # Retrieve specified number of replays
        teams_found = 0
        logger.info("Searching for teams...")
        for user_rating in user_ratings:
            # Find users replays for specified format
            logger.info(f"Retrieving {user_rating[0]}'s replays...")
            user_replay_ids = self.get_user_replay_ids(user_rating[0], format_id)
            # Skip to next user if replays not found
            if not user_replay_ids:
                logger.info("Skipping, no replays found...")
                continue
            # Find replay data using most recent replay
            logger.info("Getting replay data...")
            replay_data = self.get_replay_data(user_replay_ids[0])
            # Skip to next user if replay not found
            if not replay_data:
                logger.info("Skipping, no replay data found...")
                continue
            self.log_handler.feed(replay_data)
            self.log_handler.parse()
                # log_handler.write()
            logger.info("==Team found!==")
            teams_found += 1
            if teams_found == self.num_teams:
                break
            if teams_found == 3:
                break

        logger.info("Finished!")
