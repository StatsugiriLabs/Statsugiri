""" Log Handler is responsible for parsing metadata and replay logs into structured information """
import re
from typing import List
from base_logger import logger


class LogHandler:
    """Module for processing replay logs (ie. replay_data["logs"])"""

    def __init__(self):
        self.sanitized_log = ""

    def set_sanitized_log(self, sanitized_log: str) -> None:
        """Set sanitized replay log"""
        self.sanitized_log = sanitized_log

    def get_sanitized_log(self) -> str:
        """Get sanitized replay log"""
        return self.sanitized_log

    def feed_log(self, replay_data: dict) -> bool:
        """Clean replay data and populate metadata from log,
        Return True on success"""
        if "log" not in replay_data:
            logger.warning("Replay data does not have 'log' field, no log to feed")
            return False

        # Sanitize alternate form names, gender
        sanitized_log = replay_data["log"]
        unwanted_str_list = ["-*", ", M", ", F"]
        for unwanted_str in unwanted_str_list:
            sanitized_log = sanitized_log.replace(unwanted_str, "")
        self.set_sanitized_log(sanitized_log)
        return True

    def parse_team(self, user: str) -> List[str]:
        """Parse for teams in log"""
        if not user:
            logger.warning("Invalid username, please enter a valid user")
            return []

        sanitized_log = self.get_sanitized_log()
        if not sanitized_log:
            logger.warning("Cannot parse log for teams, log is not populated")
            return []

        # Identify if user is `p1` or `p2`
        # '|' is removed, nicknames do not affect regex
        player_num = re.findall(f"\\|player\\|(.*?)\\|{user}\\|", sanitized_log)
        if len(player_num) != 1:
            logger.warning("Could not properly locate user in log")
            return []

        player_num = player_num[0]
        team = re.findall(f"\\|poke\\|{player_num}\\|(.*?)\\|", sanitized_log)
        if not team:
            logger.warning("Cannot parse team in log, team not found")
            return []

        return team
