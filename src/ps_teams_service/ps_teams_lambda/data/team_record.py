from dataclasses import dataclass
from typing import List


@dataclass
class TeamRecord:
    team_id: str
    snapshot_date: str
    format_id: str
    pkmn_team: List[str]
    rating: int
    replay_upload_date: str
