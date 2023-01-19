from dataclasses import dataclass
from typing import List


@dataclass
class TeamInfo:
    id: str
    pkmn_team: List[str]
    rating: int
    replay_upload_date: str
