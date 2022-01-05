"""Model Handler is responsible for generating DB models and writing to storage"""
from itertools import combinations, chain
from collections import Counter
from typing import List
from replay_metadata import ParsedUserReplay
from models import PokemonTeam, PokemonTeamsSnapshot, PokemonUsageSnapshot
from constants import NUM_PARTNERS
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
            pokemon_team = PokemonTeam(
                parsed_user_replay.get_pokemon_roster(),
                parsed_user_replay.get_rating(),
                parsed_user_replay.get_replay_metadata().get_upload_time(),
            )
            pokemon_team_list.append(pokemon_team)

        return PokemonTeamsSnapshot(
            self.get_date(), self.get_format_id(), pokemon_team_list
        )

    def _calculate_pokemon_usage(self) -> dict:
        """Calculate Pokémon usage by descending"""
        pokemon_usage = {}
        pokemon_teams = [parsed_user_replay.get_pokemon_roster() for parsed_user_replay in self.get_parsed_user_replay_list()]
        # Flatten teams into one list
        flattened_pokemon_teams = list(chain(*pokemon_teams))
        # Count by frequency
        for pokemon_appearances in Counter(flattened_pokemon_teams).most_common():
            pokemon = pokemon_appearances[0]
            num_appearances = pokemon_appearances[1]
            pokemon_usage[pokemon] = num_appearances
        # Python 3.7+ preserves insertion order, hence no need to sort
        return pokemon_usage

    def _calculate_pokemon_partner_usage(self) -> dict:
        """TODO: Maybe use pokemon_usage to save on recomputing"""
        # TODO: Pokemon can just be done using set
        pokemon_partner_usage = {}
        # TODO: There's some recomputing here
        pokemon_teams = [sorted(parsed_user_replay.get_pokemon_roster()) for parsed_user_replay in self.get_parsed_user_replay_list()]
        # Flatten teams into one list
        flattened_pokemon_teams = list(chain(*pokemon_teams))
        # Identify most frequent pairings through teams by generating all pairings using `combinations`
        # Taken from: https://stackoverflow.com/questions/10844556/python-counting-frequency-of-pairs-of-elements-in-a-list-of-lists
        pokemon_pair_appearances = Counter(chain.from_iterable(combinations(pokemon_team, 2) for pokemon_team in pokemon_teams))
        # TODO: Explain what's going on
        for pokemon_appearance in Counter(flattened_pokemon_teams).most_common():
            pokemon = pokemon_appearance[0]
            pokemon_partner_usage[pokemon] = {}
            partners_found = 0
            for pokemon_pair_appearance in pokemon_pair_appearances.most_common():
                pokemon_pair = pokemon_pair_appearance[0]
                num_appearances = pokemon_pair_appearance[1]
                if pokemon in pokemon_pair:
                    # Determine which is the partner
                    pokemon_partner = pokemon_pair[1] if pokemon is pokemon_pair[0] else pokemon_pair[0]
                    pokemon_partner_usage[pokemon][pokemon_partner] = num_appearances
                    partners_found += 1
                # TODO: Replace magic number
                if partners_found == NUM_PARTNERS:
                    break

            # Break if 5 partners found
        return pokemon_partner_usage

    def make_pokemon_usage_snapshot(self) -> PokemonUsageSnapshot:
        """Generate Pokémon usage snapshot"""
        if not self.get_parsed_user_replay_list():
            logger.warning(
                "Cannot generate usage snapshot, `ParsedUserReplay` list is not populated"
            )
            return PokemonUsageSnapshot()

        # TODO: Pass in sorted pokemon_teams
        pokemon_usage = self._calculate_pokemon_usage()
        pokemon_partner_usage = self._calculate_pokemon_partner_usage()
        return PokemonUsageSnapshot(self.get_date(), self.get_format_id())
