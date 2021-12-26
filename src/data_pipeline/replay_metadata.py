""" Classes for structuring replay metadata-associated storage """
from typing import List

# pylint: disable=R0903
class ReplayMetadata:
    """Replay metadata from individual replay"""

    def __init__(self, upload_time: int, format_id: str, replay_id: str):
        self.upload_time = upload_time
        self.format_id = format_id
        self.replay_id = replay_id


# pylint: disable=R0903
class TurnInfo:
    """Individual turn information"""

    def __init__(self, turn_num: int, turn_events=str):
        self.turn_num = turn_num
        self.turn_events = turn_events


class ParsedReplay:
    """Parsed replay information from log"""

    def __init__(self):
        # Note: `battle_format` is not found in log
        self.metadata = ReplayMetadata(1, "", "")
        # str: [str] -> user and team
        self.teams = {}
        self.turn_info_list = []

    def set_replay_metadata(self, upload_time: int, format_id: str, replay_id: str):
        """Set replay metadata"""
        self.metadata = ReplayMetadata(upload_time, format_id, replay_id)

    def set_teams(
        self, p1_user: str, p2_user: str, p1_team: List[str], p2_team: List[str]
    ):
        """Set player teams"""
        self.teams[p1_user] = p1_team
        self.teams[p2_user] = p2_team

    def set_turn_info_list(self, turn_info_list: List[TurnInfo]):
        """Set turn info events list"""
        self.turn_info_list = turn_info_list

    def add_turn_info(self, turn_info: TurnInfo):
        """Add turn info to events list"""
        self.turn_info_list.append(turn_info)
