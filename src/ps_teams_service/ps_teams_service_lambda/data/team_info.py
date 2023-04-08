from dataclasses import dataclass
from typing import List


@dataclass
class TeamInfo:
    team_id: str
    pkmn_team: List[str]
    rating: int
    replay_id: str
    replay_upload_date: str
