from dataclasses import dataclass


@dataclass
class ReplayInfo:
    """Representation directly from replay JSON"""

    id: str
    username: str
    rating: int
    format: str
    log: str
    upload_time: int
