""" Data Extractor is responsible for reading format metadata and retrieving the replay JSON """
from typing import List, Tuple
import re
import time
import requests
from base_logger import logger
from bs4 import BeautifulSoup
from constants import MAX_USERS, NUM_TEAMS
from replay_metadata import ReplayMetadata, ParsedUserReplay
from log_handler import LogHandler


LADDER_BASE_URL = "https://pokemonshowdown.com/ladder/"
REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/"
REPLAY_SEARCH_BASE_URL = "https://replay.pokemonshowdown.com/search/?output=html&user="
REQUEST_TIMEOUT = 120  # [seconds]


class DataExtractor:
    """Class for ingesting, parsing, and extracting replay data"""

    def __init__(self, formats: List[str], num_teams: int = NUM_TEAMS):
        # Initialize available formats
        self.log_handler = LogHandler()
        self.formats = formats
        self.num_teams = num_teams
        self.parsed_user_replay_list = []

    def set_formats(self, formats: List[str]):
        """Set available formats"""
        self.formats = formats

    def get_formats(self) -> List[str]:
        """Get available formats"""
        return self.formats

    def set_num_teams(self, num_teams: int):
        """Set number of teams to search"""
        self.num_teams = num_teams

    def get_num_teams(self):
        """Get number of teams to search"""
        return self.num_teams

    def set_parsed_user_replay_list(
        self, parsed_user_replay_list: List[ParsedUserReplay]
    ):
        """Set parsed user replay list"""
        self.parsed_user_replay_list = parsed_user_replay_list

    def add_parsed_user_replay(self, parsed_user_replay: ParsedUserReplay):
        """Add parsed user replay to list"""
        self.parsed_user_replay_list.append(parsed_user_replay)

    def get_parsed_user_replay_list(self):
        """Get parsed user replay list"""
        return self.parsed_user_replay_list

    def get_ladder_users_and_ratings(
        self, format_id: str, num_users: int = MAX_USERS
    ) -> List[Tuple[str, int]]:
        """Return the top users and ratings within a given format"""
        ladder_get_url = LADDER_BASE_URL + format_id
        if format_id not in self.formats:
            logger.error(f"Format ({format_id}) is not found in `formats` property")
            raise ValueError(f"Format ({format_id}) is unavailable")
        if num_users > MAX_USERS:
            logger.error(
                f"Requested `num_users` ({num_users}) \
            exceeds maximum number of users ({MAX_USERS})"
            )
            raise ValueError(
                f"Maximum number of users is {MAX_USERS}, {num_users} was requested"
            )

        # Retrieve ladder HTTP response content
        logger.info("Retrieving current ladder users and ratings")
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

    # TODO: https://github.com/kelvinkoon/babiri_v2/issues/24
    def sanitize_user(self, user: str) -> str:
        """Sanitize username for non-ASCII characters and spaces"""
        # PS! ignores non-ASCII characters and spaces
        user = re.sub(r"[^\x00-\x7f]", r"", user)
        user = user.replace(" ", "")
        return user

    def get_user_replay_ids(self, user: str, format_id: str) -> List[str]:
        """Returns a user's replays by replay ID in reverse-chronological order,
        Returns blank if no replays found"""
        sanitized_user = self.sanitize_user(user)

        user_replay_ids_get_url = REPLAY_SEARCH_BASE_URL + sanitized_user
        logger.info(f"Retrieving replay IDs for '{user}'")
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

    # TODO: https://github.com/kelvinkoon/babiri_v2/issues/24
    def get_replay_data(self, replay_id: str) -> dict:
        """Returns the replay data JSON given a replay ID, blank if not found"""
        replay_data_get_url = REPLAY_BASE_URL + replay_id + ".json"
        logger.info(f"Retrieving replay data for '{replay_id}'")
        replay_data_res = requests.get(replay_data_get_url)
        return {} if not replay_data_res else replay_data_res.json()

    def extract_info(self, format_id: str) -> None:
        """Run data pipeline for extracting replay data"""
        # Commence timer recording
        start_time = time.time()

        # Retrieve top users
        logger.info("Retrieving top users...")
        user_ratings = self.get_ladder_users_and_ratings(format_id, MAX_USERS)

        # Retrieve specified number of replays
        teams_found = 0
        logger.info("Searching for teams...")
        for user_rating in user_ratings:
            user, rating = user_rating[0], user_rating[1]
            # Find users replays for specified format
            logger.info(f"Retrieving {user}'s replays...")
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

            # Feed replay data to LogHandler
            if not self.log_handler.feed_log(replay_data):
                continue

            # Gather replay metadata
            if (
                "uploadtime" not in replay_data
                or "id" not in replay_data
                or "format" not in replay_data
            ):
                continue
            upload_time, replay_id, format_id = (
                replay_data["uploadtime"],
                replay_data["id"],
                replay_data["format"],
            )

            # Populate `ReplayMetadata`
            replay_metadata = ReplayMetadata(upload_time, replay_id, format_id)

            # Populate `ParsedUserReplay` based on replay data
            user_roster = self.log_handler.parse_team(user)
            # Skip to next user if team not found
            if not user_roster:
                continue
            parsed_user_replay = ParsedUserReplay(
                replay_metadata, user, rating, user_roster
            )
            # Record team
            self.add_parsed_user_replay(parsed_user_replay)

            teams_found += 1
            if teams_found == self.num_teams:
                break

        logger.info(f"Extraction finished in {time.time() - start_time: .2f} seconds")
