""" Models for the storage layer """
import datetime
from typing import List
from constants import TEAM_SIZE, NUM_TEAMS
from base_logger import logger

class PokemonTeamSnapshot:
    """ Model for Pokémon Team Snapshots"""
    def __init__(self):
        self.date: datetime.MINYEAR
        self.format_id = ""
        self.team_list = []

    def set_date(self, date: datetime):
        self.date = date

    def get_date(self):
        return self.date

    def set_format_id(self, format_id: str):
        self.format_id = format_id

    def get_format_id(self):
        return self.format_id

    # TODO: Write test
    def set_team_list(self, team_list: List[List[str]]):
        if len(team_list) > NUM_TEAMS:
            logger.warning(f"Cannot add team list greater than maximum size of {NUM_TEAMS}")
        else:
            self.team_list = team_list

    # TODO: Write test
    def add_team(self, team: List[str]):
        if len(self.team_list) > NUM_TEAMS:
            logger.warning(f"Cannot add team, team list limited to {NUM_TEAMS}")
        else:
            self.team_list.append(team)
        
    def get_team_list(self):
        return self.team_list


class Team:
    """ Model for teams in Pokémon Team Snapshots"""
    def __init__(self):
        self.pokemon_list = []
        self.rating = 0
        self.replay_upload_date = datetime.MINYEAR

    def set_pokemon_list(self, pokemon_list: List[str]):
        """ Set Pokémon list"""
        self.pokemon_list = pokemon_list

    # TODO: Write Test
    def add_pokemon(self, pokemon: str):
        """ Add Pokémon to Pokémon list"""
        if len(self.pokemon_list) > TEAM_SIZE - 1:
            logger.warning(f"Cannot add Pokémon ({pokemon}), team list already full")
        elif pokemon in self.pokemon_list:
            logger.warning(f"Cannot add Pokémon ({pokemon}), already in team list")
        else:
            self.pokemon_list.append(pokemon)

    def get_pokemon_list(self):
        """ Get Pokémon list"""
        return self.pokemon_list

    def set_rating(self, rating: int):
        """ Set rating"""
        self.rating = rating 

    def get_rating(self):
        """ Get rating """
        return self.rating

    def set_replay_upload_date(self, replay_upload_date: datetime):
        """ Set replay upload date"""
        self.replay_upload_date = replay_upload_date

    def get_replay_upload_date(self):
        """ Get replay upload date"""
        return self.replay_upload_date
        
class PokemonUsageSnapshots:
    """ Model for Pokémon Usage Snapshots"""
    def __init__(self):
        self.date = datetime.MINYEAR
        self.format_id = ""
        # {Pokémon -> number of apperances}
        self.pokemon_usage = {}
        # {Pokémon -> {partner -> number of apperances}}
        self.pokemon_partner_usage = {}
        # {Pokémon -> average rating}
        self.pokemon_average_rating_usage = {}

    def set_date(self, date: datetime):
        self.date = date

    def get_date(self):
        return self.date

    def set_format_id(self, format_id: str):
        self.format_id = format_id

    def get_format_id(self):
        return self.format_id

    # TODO: Write test
    def set_pokemon_usage(self, pokemon: str, usage: int) -> None:
        """ Set Pokémon usage"""
        if pokemon in self.pokemon_usage:
            logger.warning(f"Pokémon ({pokemon}) already in Pokémon usage, cannot set")
        else:
            self.pokemon_usage[pokemon] = usage

    # TODO: Write test
    def get_pokemon_usage(self, pokemon: str) -> int:
        """ Get Pokémon usage"""
        if pokemon not in self.pokemon_usage:
            logger.warning("Pokémon not found in Pokémon usage, cannot retrieve")
            return 0
        else:
            return self.pokemon_usage[pokemon]

    # TODO: Write test
    def set_pokemon_partner_usage(self, pokemon: str, partner_pokemon: str, usage: int):
        """ Set Pokémon partner usage for specified Pokémon"""
        # Initialize if Pokémon not in usage
        if pokemon not in self.pokemon_partner_usage:
            self.pokemon_partner_usage[pokemon] = {}
        if partner_pokemon in self.pokemon_partner_usage[pokemon]:
            logger.warning(f"Partner Pokémon ({partner_pokemon}) already in Pokémon partner usage \
            for {pokemon}, cannot set")
        else:
            self.pokemon_partner_usage[pokemon][partner_pokemon] = usage

    # TODO: Write test
    def get_pokemon_partner_usage(self, pokemon: str, partner_pokemon: str) -> int:
        """ Get Pokémon partner usage for specified Pokémon"""
        if pokemon not in self.pokemon_partner_usage:
            logger.warning(f"Pokémon ({pokemon}) not in Pokémon partner usage, cannot retrieve")
        else:
            if partner_pokemon not in self.pokemon_partner_usage[pokemon]:
                logger.warning(f"Partner Pokémon ({partner_pokemon}) not found in Pokémon partner usage \
                for {pokemon}, cannot retrieve")
            else:
                return self.pokemon_partner_usage[pokemon][partner_pokemon]

    def set_pokemon_average_rating_usage(self, pokemon: str, rating: int) -> None:
        """ Set Pokémon average rating normalized by usage"""
        if pokemon in self.pokemon_average_rating_usage:
            logger.warning(f"Pokémon ({pokemon}) already in Pokémon average rating usage, cannot set")
        else:
            self.pokemon_average_rating_usage[pokemon] = rating

    # TODO: Write test
    def get_pokemon_average_rating_usage(self, pokemon: str) -> int:
        """ Get Pokémon average rating normalized by usage"""
        if pokemon not in self.pokemon_average_rating_usage:
            logger.warning("Pokémon not found in Pokémon average rating usage, cannot retrieve")
            return 0
        else:
            return self.pokemon_average_rating_usage[pokemon]
