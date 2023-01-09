from dataclasses import dataclass
from typing import List
from data.team_info import TeamInfo


@dataclass
class TeamSnapshot:
    """Collected teams for the date"""

    snapshot_date: str
    format_id: str
    team_list: List[TeamInfo]
