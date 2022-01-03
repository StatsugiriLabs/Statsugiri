"""Model Handler is responsible for generating DB models and writing to storage"""
from typing import List
from replay_metadata import ParsedUserReplay
from models import *

class ModelTransformer:
    def __init__(self, parsed_user_replay_list: List[ParsedUserReplay]=[], date: int=0, format_id: str=""):
        self.parsed_user_replay_list = parsed_user_replay_list
        self.date = date
        self.format_id = format_id

    def set_parsed_user_replay_list(self, parsed_user_replay_list: List[ParsedUserReplay]) -> None:
        """Set parsed user replay list"""
        self.parsed_user_replay_list = parsed_user_replay_list

    def add_parsed_user_replay(self, parsed_user_replay: ParsedUserReplay) -> None:
        """Add parsed user replay to list"""
        self.parsed_user_replay_list.append(parsed_user_replay)

    def get_parsed_user_replay_list(self) -> List[ParsedUserReplay]:
        """Get parsed user replay list"""
        return self.parsed_user_replay_list

    def set_date(self, date: int) -> None:
        """Set date"""
        self.date = date

    def get_date(self) -> int:
        """Get date"""
        return self.date

    def set_format_id(self, format_id: str) -> None:
        """Set format ID"""
        self.format_id = format_id

    def get_format_id(self) -> str:
        """Get format ID"""
        return self.format_id

    def make_pokemon_team_snapshot(self) -> PokemonTeamsSnapshot:
        """Generate Pokémon team snapshot"""
        if not self.get_parsed_user_replay_list():
            # TODO: Log error
            return None

        # Create team snapshot
        pokemon_team_list = []
        for parsed_user_replay in self.get_parsed_user_replay_list():
            # Create team metadata based on roster
            pokemon_team = PokemonTeam(parsed_user_replay.get_pokemon_roster(),
            parsed_user_replay.get_rating(), parsed_user_replay.get_replay_metadata().get_upload_time())
            pokemon_team_list.append(pokemon_team)
        return PokemonTeamsSnapshot(
            self.get_date(), self.get_format_id(), pokemon_team_list
        )
