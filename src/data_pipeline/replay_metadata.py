""" Classes for structuring replay metadata-associated storage """
from typing import List
from base_logger import logger


class ReplayMetadata:
    """Replay metadata from individual replay"""

    def __init__(self):
        self.upload_time = 0
        self.replay_id = ""
        self.format_id = ""

    def set_upload_time(self, upload_time: int) -> None:
        """Set replay upload time"""
        self.upload_time = upload_time

    def get_upload_time(self) -> int:
        """Get replay upload time"""
        return self.upload_time

    def set_replay_id(self, replay_id: str) -> None:
        """Set replay ID"""
        self.replay_id = replay_id

    def get_replay_id(self) -> str:
        """Get replay ID"""
        return self.replay_id

    def set_format_id(self, format_id: str) -> None:
        """Set replay format ID"""
        self.format_id = format_id

    def get_format_id(self) -> str:
        """Get replay format ID"""
        return self.format_id


class TurnInfo:
    """Individual turn information"""

    def __init__(self, turn_num: int, turn_events=str):
        self.turn_num = turn_num
        self.turn_events = turn_events


class ParsedReplay:
    """Parsed replay information from log"""

    def __init__(self):
        """Teams and turns populated by `LogHandler`"""
        self.metadata = ReplayMetadata()
        self.p1_user = ""
        self.p2_user = ""
        # str: [str] -> user and team
        self.teams = {}
        self.turn_info_list = []

    def set_replay_metadata(
        self, upload_time: int, format_id: str, replay_id: str
    ) -> None:
        """Set replay metadata"""
        self.metadata.set_upload_time(upload_time)
        self.metadata.set_format_id(format_id)
        self.metadata.set_replay_id(replay_id)

    def get_replay_metadata(self) -> ReplayMetadata:
        """Get replay metadata"""
        return self.metadata

    def set_p1_user(self, p1_user: str) -> None:
        """Set designated `p1` user"""
        self.p1_user = p1_user

    def get_p1_user(self) -> str:
        """Get designated `p1` user"""
        return self.p1_user

    def set_p2_user(self, p2_user: str) -> None:
        """Set designated `p2` user"""
        self.p2_user = p2_user

    def get_p2_user(self) -> str:
        """Get designated `p2` user"""
        return self.p2_user

    def set_teams(
        self, p1_user: str, p2_user: str, p1_team: List[str], p2_team: List[str]
    ) -> None:
        """Set player teams"""
        self.teams[p1_user] = p1_team
        self.teams[p2_user] = p2_team

    def get_team(self, user: str) -> List[str]:
        """Get player team given a user"""
        if user not in self.teams:
            logger.error(f"User ({user}) does not exist, team cannot be parsed")
            raise ValueError(f"User ({user}) not found in `ParsedReplay`")
        return self.teams[user]

    def set_turn_info_list(self, turn_info_list: List[TurnInfo]) -> None:
        """Set turn info events list"""
        self.turn_info_list = turn_info_list

    def add_turn_info(self, turn_info: TurnInfo) -> None:
        """Add turn info to events list"""
        self.turn_info_list.append(turn_info)
