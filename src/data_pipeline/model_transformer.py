"""Model Handler is responsible for generating DB models and writing to storage"""
from typing import List
from replay_metadata import ParsedUserReplay
from models import PokemonTeam, PokemonTeamsSnapshot
from base_logger import logger


class ModelTransformer:
    """Transforms `ParsedUserReplay` to DB models"""

    def __init__(
        self,
        parsed_user_replay_list: List[ParsedUserReplay] = None,
        date: int = 0,
        format_id: str = "",
    ):
        self.parsed_user_replay_list = (
            [] if parsed_user_replay_list is None else parsed_user_replay_list
        )
        self.date = date
        self.format_id = format_id

    def set_parsed_user_replay_list(
        self, parsed_user_replay_list: List[ParsedUserReplay]
    ) -> None:
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

    def make_pokemon_teams_snapshot(self) -> PokemonTeamsSnapshot:
        """Generate Pokémon teams snapshot"""
        if not self.get_parsed_user_replay_list():
            logger.warning(
                "Cannot generate teams snapshot, `ParsedUserReplay` list is not populated"
            )
            return PokemonTeamsSnapshot()

        # Create team snapshot
        pokemon_team_list = []
        for parsed_user_replay in self.get_parsed_user_replay_list():
            # Create team metadata based on roster
            pokemon_team = PokemonTeam()
            pokemon_team.set_pokemon_roster(parsed_user_replay.get_pokemon_roster())
            pokemon_team.set_rating(parsed_user_replay.get_rating())
            pokemon_team.set_replay_upload_date(
                parsed_user_replay.get_replay_metadata().get_upload_time()
            )
            pokemon_team_list.append(pokemon_team)

        pokemon_teams_snapshot = PokemonTeamsSnapshot()
        pokemon_teams_snapshot.set_date(self.get_date())
        pokemon_teams_snapshot.set_format_id(self.get_format_id())
        pokemon_teams_snapshot.set_pokemon_team_list(pokemon_team_list)
        return pokemon_teams_snapshot
