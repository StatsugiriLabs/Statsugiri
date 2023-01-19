from dataclasses import dataclass


@dataclass
class PsIngestConfig:
    snapshot_date: str
    format_id: str
    num_replays_to_pull: int
