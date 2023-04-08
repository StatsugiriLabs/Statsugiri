from dataclasses import dataclass
from typing import List
from .team_info import TeamInfo


@dataclass
class GetTeamsResponse:
    num_teams: int
    format_id: str
    snapshot_date: str
    teams: List[TeamInfo]
