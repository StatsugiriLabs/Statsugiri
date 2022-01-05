"""Unit tests for `ModelTransformer` class"""
import pytest
from typing import List
from models import PokemonTeamsSnapshot, PokemonTeam
from replay_metadata import ParsedUserReplay, ReplayMetadata
from model_transformer import ModelTransformer

DATE = 12
FORMAT = "gen8vgc2021series11"
UPLOAD_DATE_1 = 1
RATING_1 = 1
UPLOAD_DATE_2 = 2
RATING_2 = 2


@pytest.fixture(name="model_transformer_under_test")
def fixture_model_transformer():
    """Initialize model transformer for tests"""
    parsed_user_replay_list_data = [
        {
            "replay_metadata": ReplayMetadata(UPLOAD_DATE_1, "replay_id_1"),
            "user": "user1",
            "rating": RATING_1,
            "pokemon_roster": ["pkmn1-1", "pkmn1-2", "pkmn1-3"],
        },
        {
            "replay_metadata": ReplayMetadata(UPLOAD_DATE_2, "replay_id_2"),
            "user": "user2",
            "rating": RATING_2,
            "pokemon_roster": ["pkmn2-1", "pkmn2-2", "pkmn2-3"],
        },
    ]
    # Populate `parsed_user_replay_list`
    parsed_user_replay_list = []
    for parsed_user_replay_data in parsed_user_replay_list_data:
        parsed_user_replay_list.append(
            ParsedUserReplay(
                parsed_user_replay_data["replay_metadata"],
                parsed_user_replay_data["user"],
                parsed_user_replay_data["rating"],
                parsed_user_replay_data["pokemon_roster"],
            )
        )

    return ModelTransformer(parsed_user_replay_list, DATE, FORMAT)


def verify_pokemon_teams_snapshot_match(
    pokemon_teams_snapshot: PokemonTeamsSnapshot,
    expected_pokemon_teams_snapshot: PokemonTeamsSnapshot,
):
    """Check if two `PokémonTeamSnapshot` objects match"""
    assert (
        pokemon_teams_snapshot.get_date() == expected_pokemon_teams_snapshot.get_date()
    )
    assert (
        pokemon_teams_snapshot.get_format_id()
        == expected_pokemon_teams_snapshot.get_format_id()
    )
    verify_pokemon_team_match(
        pokemon_teams_snapshot.get_pokemon_team_list(),
        expected_pokemon_teams_snapshot.get_pokemon_team_list(),
    )


def verify_pokemon_team_match(
    pokemon_team_list: List[PokemonTeam], expected_pokemon_team_list: List[PokemonTeam]
):
    """Check if two `PokemonTeam` objects match"""
    assert len(pokemon_team_list) == len(expected_pokemon_team_list)
    for i in range(len(pokemon_team_list)):
        assert (
            pokemon_team_list[i].get_pokemon_roster()
            == expected_pokemon_team_list[i].get_pokemon_roster()
        )
        assert (
            pokemon_team_list[i].get_rating()
            == expected_pokemon_team_list[i].get_rating()
        )
        assert (
            pokemon_team_list[i].get_replay_upload_date()
            == expected_pokemon_team_list[i].get_replay_upload_date()
        )


def test_model_transformer_make_pokemon_teams_snapshot_happy_path(
    model_transformer_under_test,
):
    """Test model transformer generating `PokemonTeamSnapshot` list"""
    pokemon_team_1 = PokemonTeam(
        ["pkmn1-1", "pkmn1-2", "pkmn1-3"], RATING_1, UPLOAD_DATE_1
    )
    pokemon_team_2 = PokemonTeam(
        ["pkmn2-1", "pkmn2-2", "pkmn2-3"], RATING_2, UPLOAD_DATE_2
    )
    expected_pokemon_teams_snapshot = PokemonTeamsSnapshot(
        DATE, FORMAT, [pokemon_team_1, pokemon_team_2]
    )
    pokemon_teams_snapshot = model_transformer_under_test.make_pokemon_teams_snapshot()
    verify_pokemon_teams_snapshot_match(
        pokemon_teams_snapshot, expected_pokemon_teams_snapshot
    )
