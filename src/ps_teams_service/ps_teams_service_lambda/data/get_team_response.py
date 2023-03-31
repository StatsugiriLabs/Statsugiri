from dataclasses import dataclass
from .team_info import TeamInfo


@dataclass
class GetTeamResponse:
    team: TeamInfo
