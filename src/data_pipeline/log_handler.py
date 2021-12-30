""" Log Handler is responsible for parsing metadata and replay logs into structured information """
import re
from replay_metadata import ParsedReplay
from base_logger import logger

class LogHandler:
    def __init__(self):
        self.parsed_replay = ParsedReplay()
        # TODO: Transformers will make use of ParsedReplay state from `data_extractor`` layer

    def feed(self, replay_data: dict):
        """ Clean replay data and populate metadata from log """
        # Sanitize alternate form names
        sanitized_log = replay_data["log"].replace("-*", "")
        self.parsed_replay.set_sanitized_log(sanitized_log)
        # Add replay metadata
        # Issue #38
        self.parsed_replay.set_replay_metadata(replay_data["uploadtime"], replay_data["formatid"], replay_data["id"])

    def parse_users(self) -> bool:
        """ Parse for players and store in `parsed_replay` """
        """ Return True if users successfully parsed, False otherwise """
        sanitized_log = self.parsed_replay.get_sanitized_log()
        if not sanitized_log:
            logger.warn("Cannot parse log for users, log is not populated")
            return False

        p1_user = re.findall("\\|player\\|p1\\|(.*?)\\|", sanitized_log)[0]
        p2_user = re.findall("\\|player\\|p2\\|(.*?)\\|", sanitized_log)[0]
        if not p1_user or not p2_user:
            logger.warn(f"Cannot parse a user in log ({self.parsed_replay.get_replay_metadata().get_replay_id()})")
            return False

        self.parsed_replay.set_p1_user(p1_user)
        self.parsed_replay.set_p2_user(p2_user)
        return True

    def parse_teams(self) -> bool:
        """ Parse for teams and store in `parsed_replay` """
        """ Return True if teams successfully parsed, False otherwise """
        sanitized_log = self.parsed_replay.get_sanitized_log()
        if not sanitized_log:
            logger.warn("Cannot parse log for teams, log is not populated")
            return False

        p1_team = re.findall("\\|poke\\|p1\\|(.*?),", sanitized_log)
        p2_team = re.findall("\\|poke\\|p2\\|(.*?),", sanitized_log)
        if not p1_team or not p2_team:
            logger.warn("Cannot parse teams in log, teams not found")
            return False

        p1_user = self.parsed_replay.get_p1_user()
        p2_user = self.parsed_replay.get_p2_user()
        if not p1_user or not p2_user:
            logger.warn("Cannot parse teams in log, users have not been parsed")
            return False

        self.parsed_replay.set_teams(p1_user, p2_user, p1_team, p2_team)
        return True

    def parse(self) -> bool:
        """ Transform and store cleaned log into `ParsedReplay` data """
        """ Return True if replay data successfully parsed """
        return self.parse_users() and self.parse_teams()
