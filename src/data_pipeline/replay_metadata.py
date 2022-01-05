""" Classes for structuring replay metadata-associated storage """
from typing import List


class ReplayMetadata:
    """Replay metadata from individual replay"""

    def __init__(self, upload_time: int, replay_id: str):
        self.upload_time = upload_time
        self.replay_id = replay_id

    def set_upload_time(self, upload_time: int) -> None:
        """Set replay upload time"""
        self.upload_time = upload_time

    def get_upload_time(self) -> int:
        """Get replay upload time"""
        return self.upload_time

    def set_replay_id(self, replay_id: str) -> None:
        """Set replay ID"""
        self.replay_id = replay_id

    def get_replay_id(self) -> str:
        """Get replay ID"""
        return self.replay_id


class ParsedUserReplay:
    """Parsed replay information from log"""

    def __init__(
        self,
        replay_metadata: ReplayMetadata,
        rating: int,
        pokemon_roster: List[str],
    ):
        """Teams and turns populated by `LogHandler`"""
        self.metadata = replay_metadata
        self.rating = rating
        self.pokemon_roster = pokemon_roster

    def set_replay_metadata(self, replay_metadata: ReplayMetadata) -> None:
        """Set replay metadata"""
        self.metadata = replay_metadata

    def get_replay_metadata(self) -> ReplayMetadata:
        """Get replay metadata"""
        return self.metadata

    def set_rating(self, rating: int) -> None:
        """Set rating"""
        self.rating = rating

    def get_rating(self) -> int:
        """Get rating"""
        return self.rating

    def set_pokemon_roster(self, pokemon_roster: List[str]) -> None:
        """Set Pokémon roster"""
        self.pokemon_roster = pokemon_roster

    def get_pokemon_roster(self) -> List[str]:
        """Get Pokémon roster"""
        return self.pokemon_roster
