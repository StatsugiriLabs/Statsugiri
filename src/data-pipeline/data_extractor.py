""" Data Extractor is responsible for reading format metadata and retrieving the replay JSON """
from typing import List
import requests
from bs4 import BeautifulSoup
from constants import MAX_USERS


LADDER_BASE_URL = "https://pokemonshowdown.com/ladder/"
REQUEST_TIMEOUT = 60


class DataExtractor:
    """Class for ingesting, parsing, and extracting replay data"""

    def __init__(self, formats: List[str], num_teams: int = 100):
        # Initialize available formats
        self.formats = formats
        # self.replay_parser = ReplayParser()
        self.num_teams = num_teams

    def get_formats(self):
        """Return available formats"""
        return self.formats

    def get_ladder_users_and_ratings(
        self, battle_format: str, num_users: int = MAX_USERS
    ) -> list[str, int]:
        """Return the top X users within a given format"""
        if battle_format not in self.formats:
            raise ValueError("Format is unavailable")
        if num_users > MAX_USERS:
            raise ValueError(
                f"Maximum number of users is {MAX_USERS}, {num_users} was requested"
            )

        # Retrieve ladder HTTP response content
        ladder_res = requests.get(
            LADDER_BASE_URL + battle_format, timeout=REQUEST_TIMEOUT
        )
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

    # def get_replay_parser_name(self):
    #     return self.replay_parser.get_name()

    # def set_replay_parser(self, replay_parser: ReplayParser):
    #     self.parser = replay_parser

    # def extract_info(self, battle_format: str):
    #     """Run data pipeline for extracting replay data"""
    #     # Retrieve top users
    #     users = self.get_ladder_users_and_ratings(battle_format, 10)
