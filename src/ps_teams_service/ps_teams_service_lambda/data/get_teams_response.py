from dataclasses import dataclass
from typing import List
from team_info import TeamInfo


@dataclass
class GetTeamsResponse:
    page: int
    teams: List[TeamInfo]
