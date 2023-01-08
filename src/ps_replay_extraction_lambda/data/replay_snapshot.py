from dataclasses import dataclass
from typing import List
from data.replay_info import ReplayInfo


@dataclass
class ReplaySnapshot:
    """Collected replays for the date"""

    snapshot_date: str
    format_id: str
    replay_list: List[ReplayInfo]
