from dataclasses import dataclass


@dataclass
class IngestDataInfo:
    snapshot_date: str
    num_users_to_pull: int
