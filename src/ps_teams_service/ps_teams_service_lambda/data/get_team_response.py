from dataclasses import dataclass
from .team_info import TeamInfo


@dataclass
class GetTeamResponse:
    format_id: str
    snapshot_date: str
    team: TeamInfo
