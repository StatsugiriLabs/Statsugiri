"""Model Transformer is responsible for generating DB models"""
from itertools import combinations, chain
from collections import Counter
from typing import List, Dict
from replay_metadata import ParsedUserReplay
from models import PokemonTeam, PokemonTeamsSnapshot, PokemonUsageSnapshot
from constants import NUM_PARTNERS
from base_logger import logger
from utils import convert_unix_timestamp_to_str


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
        # Output models will have 'yyyy-mm-dd' string format
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

    def make_pokemon_teams_snapshot_model(self) -> dict:
        """Generate Pokémon teams snapshot model"""
        if not self.get_parsed_user_replay_list():
            logger.warning(
                "Cannot generate teams snapshot, `ParsedUserReplay` list is not populated"
            )
            return {}

        # Create team snapshot
        pokemon_team_list = []
        for parsed_user_replay in self.get_parsed_user_replay_list():
            # Create team metadata based on roster
            pokemon_team = PokemonTeam(
                parsed_user_replay.get_pokemon_roster(),
                parsed_user_replay.get_rating(),
                convert_unix_timestamp_to_str(
                    parsed_user_replay.get_replay_metadata().get_upload_time()
                ),
            )
            pokemon_team_list.append(pokemon_team)

        return PokemonTeamsSnapshot(
            convert_unix_timestamp_to_str(self.get_date()),
            self.get_format_id(),
            pokemon_team_list,
        ).make_model()

    def _calculate_pokemon_usage(self, pokemon_teams: List[List[str]]) -> dict:
        """Calculate Pokémon usage by descending"""
        if not pokemon_teams:
            return {}

        pokemon_usage = {}
        # Flatten teams into one list
        flattened_pokemon_teams = list(chain(*pokemon_teams))
        # Record by frequency
        for pokemon_appearances in Counter(flattened_pokemon_teams).most_common():
            pokemon = pokemon_appearances[0]
            num_appearances = pokemon_appearances[1]
            pokemon_usage[pokemon] = num_appearances

        return pokemon_usage

    def _calculate_pokemon_partner_usage(self, pokemon_teams: List[List[str]]) -> dict:
        """Calculate Pokémon partner usage by descending"""
        if not pokemon_teams:
            return {}

        pokemon_partner_usage: Dict[str, Dict[str, int]] = {}
        # Flatten teams into one list
        flattened_pokemon_teams = list(chain(*pokemon_teams))
        """
        Identify most frequent pairings through teams by
        generating all pairings using `combinations`
        https://stackoverflow.com/questions/10844556/
        python-counting-frequency-of-pairs-of-elements-in-a-list-of-lists
        """
        all_pokemon_pair_appearances = Counter(
            chain.from_iterable(
                combinations(pokemon_team, 2) for pokemon_team in pokemon_teams
            )
        )

        # Search Pokémon from most common appearance
        for pokemon_appearance in Counter(flattened_pokemon_teams).most_common():
            pokemon = pokemon_appearance[0]
            pokemon_partner_usage[pokemon] = {}
            partners_found = 0
            # Find partners by most common appearance
            for pokemon_pair_appearance in all_pokemon_pair_appearances.most_common():
                pokemon_pair = pokemon_pair_appearance[0]
                num_appearances = pokemon_pair_appearance[1]
                # If found in pair, record until `NUM_PARTNERS` found
                if pokemon in pokemon_pair:
                    # Determine which is the partner
                    pokemon_partner = (
                        pokemon_pair[1]
                        if pokemon == pokemon_pair[0]
                        else pokemon_pair[0]
                    )
                    pokemon_partner_usage[pokemon][pokemon_partner] = num_appearances
                    partners_found += 1
                if partners_found == NUM_PARTNERS:
                    break

        return pokemon_partner_usage

    def _calculate_pokemon_average_rating_usage(
        self, pokemon_teams: List[List[str]]
    ) -> dict:
        """Calculate Pokémon average rating usage by descending"""
        if not pokemon_teams:
            return {}

        # Get all replays with Pokemon
        pokemon_average_rating_usage = {}
        # Flatten teams into one list
        flattened_pokemon_teams = list(chain(*pokemon_teams))
        # Record by frequency
        for pokemon_appearances in Counter(flattened_pokemon_teams).most_common():
            # Filter for parsed replays featuring Pokémon
            pokemon = pokemon_appearances[0]
            filtered_parsed_user_replay_list = list(
                filter(
                    lambda parsed_user_replay: (
                        pokemon in parsed_user_replay.get_pokemon_roster()
                    ),
                    self.get_parsed_user_replay_list(),
                )
            )
            # Calculate average rating
            average_rating = sum(
                [
                    parsed_user_replay.get_rating()
                    for parsed_user_replay in filtered_parsed_user_replay_list
                ]
            ) // len(filtered_parsed_user_replay_list)
            pokemon_average_rating_usage[pokemon] = average_rating

        return pokemon_average_rating_usage

    def make_pokemon_usage_snapshot_model(self) -> dict:
        """Generate Pokémon usage snapshot model"""
        if not self.get_parsed_user_replay_list():
            logger.warning(
                "Cannot generate usage snapshot, `ParsedUserReplay` list is not populated"
            )
            return {}

        pokemon_teams = [
            sorted(parsed_user_replay.get_pokemon_roster())
            for parsed_user_replay in self.get_parsed_user_replay_list()
        ]
        pokemon_usage = self._calculate_pokemon_usage(pokemon_teams)
        pokemon_partner_usage = self._calculate_pokemon_partner_usage(pokemon_teams)
        pokemon_average_rating_usage = self._calculate_pokemon_average_rating_usage(
            pokemon_teams
        )

        return PokemonUsageSnapshot(
            convert_unix_timestamp_to_str(self.get_date()),
            self.get_format_id(),
            pokemon_usage,
            pokemon_partner_usage,
            pokemon_average_rating_usage,
        ).make_model()
