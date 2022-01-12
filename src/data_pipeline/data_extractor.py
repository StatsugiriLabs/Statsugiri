""" Data Extractor is responsible for reading format metadata and retrieving the replay logs """
from typing import List, Tuple
import re
import time
import requests
import mypy_boto3_dynamodb as boto3_dynamodb
from base_logger import logger
from bs4 import BeautifulSoup
from constants import (
    MAX_USERS,
    NUM_TEAMS,
)
from db_utils import (
    write_pokemon_teams_snapshots_table,
    write_pokemon_usage_snapshots_table,
)
from model_transformer import ModelTransformer
from replay_metadata import ReplayMetadata, ParsedUserReplay
from log_handler import LogHandler


LADDER_BASE_URL = "https://pokemonshowdown.com/ladder/"
REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/"
REPLAY_SEARCH_BASE_URL = "https://replay.pokemonshowdown.com/search/?output=html&user="
REQUEST_TIMEOUT = 120  # [seconds]


class DataExtractor:
    """Class for ingesting, parsing, and extracting replay data"""

    def __init__(
        self,
        dynamodb_resource: boto3_dynamodb.DynamoDBServiceResource,
        date: int = 0,
        formats: List[str] = None,
        num_teams: int = NUM_TEAMS,
    ):
        self.log_handler = LogHandler()
        self.dynamodb_resource = dynamodb_resource
        self.date = date
        self.formats = [] if formats is None else formats
        self.num_teams = num_teams
        self.parsed_user_replay_list: List[ParsedUserReplay] = []

    def set_dynamodb_resource(
        self, dynamodb_resource: boto3_dynamodb.DynamoDBServiceResource
    ) -> None:
        """Set DynamoDB resource"""
        self.dynamodb_resource = dynamodb_resource

    def get_dynamodb_resource(self) -> boto3_dynamodb.DynamoDBServiceResource:
        """Get DynamoDB resource"""
        return self.dynamodb_resource

    def set_date(self, date: int) -> None:
        """Set date"""
        self.date = date

    def get_date(self) -> int:
        """Get date"""
        return self.date

    def set_formats(self, formats: List[str]) -> None:
        """Set available formats"""
        self.formats = formats

    def get_formats(self) -> List[str]:
        """Get available formats"""
        return self.formats

    def set_num_teams(self, num_teams: int) -> None:
        """Set number of teams to search"""
        self.num_teams = num_teams

    def get_num_teams(self) -> int:
        """Get number of teams to search"""
        return self.num_teams

    def set_parsed_user_replay_list(
        self, parsed_user_replay_list: List[ParsedUserReplay]
    ) -> None:
        """Set parsed user replay list"""
        self.parsed_user_replay_list = parsed_user_replay_list

    def add_parsed_user_replay(self, parsed_user_replay: ParsedUserReplay) -> None:
        """Add parsed user replay to list"""
        self.parsed_user_replay_list.append(parsed_user_replay)

    def get_parsed_user_replay_list(self) -> List[ParsedUserReplay]:
        """Get parsed user replay list"""
        return self.parsed_user_replay_list

    def get_ladder_users_and_ratings(
        self, format_id: str, num_users: int = MAX_USERS
    ) -> List[Tuple[str, int]]:
        """Return the top users and ratings within a given format"""
        if format_id not in self.get_formats():
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
        ladder_get_url = LADDER_BASE_URL + format_id
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

    def _sanitize_user(self, user: str) -> str:
        """Sanitize username for non-ASCII characters and spaces"""
        # PS! ignores non-ASCII characters and spaces
        user = re.sub(r"[^\x00-\x7f]", r"", user)
        user = user.replace(" ", "")
        return user

    def get_user_replay_ids(self, user: str, format_id: str) -> List[str]:
        """Returns a user's replays by replay ID in reverse-chronological order,
        Returns blank if no replays found"""
        sanitized_user = self._sanitize_user(user)

        user_replay_ids_get_url = REPLAY_SEARCH_BASE_URL + sanitized_user
        logger.info(f"Retrieving replay IDs for '{user}'")
        user_replays_res = requests.get(
            user_replay_ids_get_url, timeout=REQUEST_TIMEOUT
        )
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

    def _get_replay_data(self, replay_id: str) -> dict:
        """Returns the replay data JSON given a replay ID, blank if not found"""
        replay_data_get_url = REPLAY_BASE_URL + replay_id + ".json"
        logger.info(f"Retrieving replay data for '{replay_id}'")
        replay_data_res = requests.get(replay_data_get_url, timeout=REQUEST_TIMEOUT)
        return {} if not replay_data_res else replay_data_res.json()

    def _extract_parsed_user_replay(
        self, user: str, rating: int, format_id: str
    ) -> Tuple[ParsedUserReplay, bool]:
        """Extract replay metadata and log information into `ParsedUserReplay`
        Return True on success, False otherwise"""
        logger.info(f"Retrieving {user}'s replays...")
        user_replay_ids = self.get_user_replay_ids(user, format_id)
        # Skip to next user if replays not found
        if not user_replay_ids:
            logger.info("Skipping, no replays found...")
            return (ParsedUserReplay(), False)

        # Find replay data using most recent replay
        logger.info("Getting replay data...")
        replay_data = self._get_replay_data(user_replay_ids[0])
        # Skip to next user if replay not found or metadata tags not found
        if not replay_data or (
            "uploadtime" not in replay_data or "id" not in replay_data
        ):
            logger.info("Skipping, replay data invalid or not found...")
            return (ParsedUserReplay(), False)

        # Feed replay data to LogHandler
        if not self.log_handler.feed_log(replay_data):
            logger.info("Skipping, feeding log failed")
            return (ParsedUserReplay(), False)

        # Populate `ReplayMetadata`
        replay_metadata = ReplayMetadata(replay_data["uploadtime"], replay_data["id"])

        # Populate `ParsedUserReplay` based on replay data
        user_roster = self.log_handler.parse_team(user)
        # Skip to next user if team not found
        if not user_roster:
            logger.info("Skipping, team could not be found")
            return (ParsedUserReplay(), False)

        return (ParsedUserReplay(replay_metadata, rating, user_roster), True)

    def _write_snapshots(
        self,
        pokemon_teams_snapshot_model: dict,
        pokemon_usage_snapshot_model: dict,
    ) -> None:
        """Write snapshots to storage"""
        write_pokemon_teams_snapshots_table(
            self.dynamodb_resource, pokemon_teams_snapshot_model
        )
        write_pokemon_usage_snapshots_table(
            self.dynamodb_resource, pokemon_usage_snapshot_model
        )

    def extract_info(self, format_id: str) -> dict:
        """Run data pipeline for extracting replay data"""
        # Commence timer recording
        start_time = time.time()

        # Retrieve top users
        logger.info("Retrieving top users...")
        user_ratings = self.get_ladder_users_and_ratings(format_id, MAX_USERS)
        if not user_ratings:
            logger.warning("Could not retrieve ladder rankings, aborting...")
            return False

        # Retrieve specified number of replays
        teams_found = 0
        logger.info("Searching for teams...")

        # Parse replay to populate `ParsedUserReplay`
        for user, rating in user_ratings:
            parsed_user_replay, success = self._extract_parsed_user_replay(
                user, rating, format_id
            )
            # If unsuccessful, skip to next user
            if success:
                self.add_parsed_user_replay(parsed_user_replay)
                teams_found += 1
                if teams_found == self.num_teams:
                    break

        # Configure model transformer
        model_transformer = ModelTransformer(
            self.get_parsed_user_replay_list(), self.get_date(), format_id
        )
        pokemon_teams_snapshot_model = (
            model_transformer.make_pokemon_teams_snapshot_model()
        )
        pokemon_usage_snapshot_model = (
            model_transformer.make_pokemon_usage_snapshot_model()
        )

        # Write to storage
        self._write_snapshots(
            pokemon_teams_snapshot_model, pokemon_usage_snapshot_model
        )

        logger.info(f"Processing finished in {time.time() - start_time: .2f} seconds")
        return {
            "pokemon_teams_snapshot_model": pokemon_teams_snapshot_model,
            "pokemon_usage_snapshot_model": pokemon_usage_snapshot_model,
        }
