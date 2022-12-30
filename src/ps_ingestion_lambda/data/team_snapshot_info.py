from dataclasses import dataclass
from typing import List


@dataclass
class TeamSnapshotInfo:
    id: str
    pkmn_team: List[str]
    snapshot_date: str
    rating: int
    replay_upload_date: str
    format: str
