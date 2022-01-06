"""Unit tests for `ModelTransformer` class"""
import pytest
from typing import List
from models import PokemonTeamsSnapshot, PokemonTeam, PokemonUsageSnapshot
from replay_metadata import ParsedUserReplay, ReplayMetadata
from model_transformer import ModelTransformer

DATE = 12
FORMAT = "gen8vgc2021series11"
UPLOAD_DATE_1 = 1
RATING_1 = 1
ROSTER_1 = ["pkmn_a", "pkmn_b", "pkmn_c"]
UPLOAD_DATE_2 = 2
RATING_2 = 2
ROSTER_2 = ["pkmn_b", "pkmn_c", "pkmn_d"]
UPLOAD_DATE_3 = 3
RATING_3 = 3
ROSTER_3 = ["pkmn_b", "pkmn_c", "pkmn_e"]


@pytest.fixture(name="model_transformer_under_test")
def fixture_model_transformer():
    """Initialize model transformer for tests"""
    parsed_user_replay_list_data = [
        {
            "replay_metadata": ReplayMetadata(UPLOAD_DATE_1, "replay_id_1"),
            "rating": RATING_1,
            "pokemon_roster": ROSTER_1,
        },
        {
            "replay_metadata": ReplayMetadata(UPLOAD_DATE_2, "replay_id_2"),
            "rating": RATING_2,
            "pokemon_roster": ROSTER_2,
        },
        {
            "replay_metadata": ReplayMetadata(UPLOAD_DATE_3, "replay_id_3"),
            "rating": RATING_3,
            "pokemon_roster": ROSTER_3,
        },
    ]
    # Populate `parsed_user_replay_list`
    parsed_user_replay_list = []
    for parsed_user_replay_data in parsed_user_replay_list_data:
        parsed_user_replay_list.append(
            ParsedUserReplay(
                parsed_user_replay_data["replay_metadata"],
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
    pokemon_team_1 = PokemonTeam(ROSTER_1, RATING_1, UPLOAD_DATE_1)
    pokemon_team_2 = PokemonTeam(ROSTER_2, RATING_2, UPLOAD_DATE_2)
    pokemon_team_3 = PokemonTeam(ROSTER_3, RATING_3, UPLOAD_DATE_3)
    expected_pokemon_teams_snapshot = PokemonTeamsSnapshot(
        DATE, FORMAT, [pokemon_team_1, pokemon_team_2, pokemon_team_3]
    )
    pokemon_teams_snapshot = model_transformer_under_test.make_pokemon_teams_snapshot()
    verify_pokemon_teams_snapshot_match(
        pokemon_teams_snapshot, expected_pokemon_teams_snapshot
    )


def verify_pokemon_usage_snapshot_match(
    pokemon_usage_snapshot: PokemonUsageSnapshot,
    expected_pokemon_usage_snapshot: PokemonUsageSnapshot,
):
    """Check if two `PokemonUsageSnapshot` objects match"""
    assert (
        pokemon_usage_snapshot.get_date() == expected_pokemon_usage_snapshot.get_date()
    )
    assert (
        pokemon_usage_snapshot.get_format_id()
        == expected_pokemon_usage_snapshot.get_format_id()
    )
    assert (
        pokemon_usage_snapshot.get_all_pokemon_usage()
        == expected_pokemon_usage_snapshot.get_all_pokemon_usage()
    )
    assert (
        pokemon_usage_snapshot.get_all_pokemon_partner_usage()
        == expected_pokemon_usage_snapshot.get_all_pokemon_partner_usage()
    )
    assert (
        pokemon_usage_snapshot.get_all_pokemon_average_rating_usage()
        == expected_pokemon_usage_snapshot.get_all_pokemon_average_rating_usage()
    )


def test_model_transformer_make_pokemon_usage_snapshot_happy_path(
    model_transformer_under_test,
):
    """Test model transformer generating `PokemonUsageSnapshot` list"""
    pokemon_usage = {"pkmn_b": 3, "pkmn_c": 3, "pkmn_a": 1, "pkmn_d": 1, "pkmn_e": 1}
    pokemon_partner_usage = {
        "pkmn_b": {"pkmn_c": 3, "pkmn_a": 1, "pkmn_d": 1, "pkmn_e": 1},
        "pkmn_c": {"pkmn_b": 3, "pkmn_a": 1, "pkmn_d": 1, "pkmn_e": 1},
        "pkmn_a": {"pkmn_b": 1, "pkmn_c": 1},
        "pkmn_d": {"pkmn_b": 1, "pkmn_c": 1},
        "pkmn_e": {"pkmn_b": 1, "pkmn_c": 1},
    }
    pokemon_average_rating_usage = {
        "pkmn_e": 3.0,
        "pkmn_b": 2.0,
        "pkmn_c": 2.0,
        "pkmn_d": 2.0,
        "pkmn_a": 1.0,
    }
    expected_pokemon_usage_snapshot = PokemonUsageSnapshot(
        DATE, FORMAT, pokemon_usage, pokemon_partner_usage, pokemon_average_rating_usage
    )
    pokemon_usage_snapshot = model_transformer_under_test.make_pokemon_usage_snapshot()
    verify_pokemon_usage_snapshot_match(
        pokemon_usage_snapshot, expected_pokemon_usage_snapshot
    )


def test_model_transformer_make_pokemon_teams_snapshot_empty_parsed_user_replay_list_should_return_empty_snapshot():
    model_transformer_under_test = ModelTransformer()
    empty_snapshot = model_transformer_under_test.make_pokemon_teams_snapshot()
    verify_pokemon_teams_snapshot_match(empty_snapshot, PokemonTeamsSnapshot())


def test_model_transformer_make_pokemon_usage_snapshot_empty_parsed_user_replay_list_should_return_empty_snapshot():
    model_transformer_under_test = ModelTransformer()
    empty_snapshot = model_transformer_under_test.make_pokemon_usage_snapshot()
    verify_pokemon_usage_snapshot_match(empty_snapshot, PokemonUsageSnapshot())


def test_model_transformer_calculate_pokemon_stats_empty_teams_should_return_empty_dictionary(
    model_transformer_under_test,
):
    assert model_transformer_under_test._calculate_pokemon_usage([]) == {}
    assert model_transformer_under_test._calculate_pokemon_partner_usage([]) == {}
    assert (
        model_transformer_under_test._calculate_pokemon_average_rating_usage([]) == {}
    )
