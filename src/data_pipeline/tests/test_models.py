""" Unit tests for models (ie. getters / setters with non-trivial logic)"""
import pytest
from models import PokemonTeamsSnapshot, PokemonUsageSnapshot, PokemonTeam
from constants import NUM_TEAMS, TEAM_SIZE


@pytest.fixture(name="pokemon_team_snapshot_under_test")
def fixture_pokemon_team_snapshot():
    """Initialize Pokémon team snapshot object"""
    return PokemonTeamsSnapshot()

@pytest.fixture(name="pokemon_team_under_test")
def fixture_pokemon_team():
    """Initialize team object"""
    return PokemonTeam()


@pytest.fixture(name="pokemon_usage_snapshot_under_test")
def fixture_pokemon_usage_snapshot_under_test():
    """Initialize Pokémon usage snapshot object"""
    return PokemonUsageSnapshot()

def test_pokemon_team_snapshot_set_team_list_happy_path(
    pokemon_team_snapshot_under_test,
):
    """Test setting team list successfully"""
    teams = [
        ["pkmn1a", "pkmn1b", "pkmn1c"],
        ["pkmn2a", "pkmn2b", "pkmn2c"],
        ["pkmn3a", "pkmn3b", "pkmn3c"],
        ["pkmn4a", "pkmn4b", "pkmn4c"],
    ]
    pokemon_team_snapshot_under_test.set_team_list(teams)
    assert pokemon_team_snapshot_under_test.get_team_list() == teams


def test_pokemon_team_snapshot_set_team_list_exceeds_size_should_not_set(
    pokemon_team_snapshot_under_test,
):
    """Test setting team when provided team exceeds size"""
    # Exceed maximum allotted number of teams
    teams = [["pkmn1a", "pkmn1b", "pkmn1c"] for _ in range(NUM_TEAMS + 1)]
    pokemon_team_snapshot_under_test.set_team_list(teams)
    assert pokemon_team_snapshot_under_test.get_team_list() == []


def test_pokemon_team_snapshot_add_team_happy_path(pokemon_team_snapshot_under_test):
    """Test adding team successfully"""
    new_team = ["newpkmn1a", "newpkmn1b", "newpkmn1c"]
    pokemon_team_snapshot_under_test.add_team(new_team)
    assert pokemon_team_snapshot_under_test.get_team_list() == [new_team]


def test_pokemon_team_snapshot_add_team_full_should_not_add(
    pokemon_team_snapshot_under_test,
):
    """Test adding Pokémon when team list is full"""
    # breakpoint()
    teams = [["pkmn1a", "pkmn1b", "pkmn1c"] for i in range(NUM_TEAMS + 1)]
    for team in teams:
        pokemon_team_snapshot_under_test.add_team(team)
    assert pokemon_team_snapshot_under_test.get_team_list() == teams[:NUM_TEAMS]


def test_pokemon_team_set_pokemon_roster_happy_path(pokemon_team_under_test):
    team = ["pkmn1", "pkmn2", "pkmn3"]
    pokemon_team_under_test.set_pokemon_roster(team)
    assert pokemon_team_under_test.get_pokemon_roster() == team


def test_pokemon_team_set_pokemon_roster_exceeds_size_should_not_set(
    pokemon_team_under_test,
):
    team = ["pkmn" + str(i + 1) for i in range(TEAM_SIZE + 1)]
    pokemon_team_under_test.set_pokemon_roster(team)
    assert pokemon_team_under_test.get_pokemon_roster() == []


def test_pokemon_team_add_pokemon_happy_path(pokemon_team_under_test):
    """Test adding Pokémon to team successfully"""
    pokemon_team_under_test.add_pokemon("pkmn1")
    pokemon_team_under_test.add_pokemon("pkmn2")
    assert pokemon_team_under_test.get_pokemon_roster() == ["pkmn1", "pkmn2"]


def test_pokemon_team_add_pokemon_full_should_not_add(pokemon_team_under_test):
    """Test adding Pokémon to team when the team roster is full"""
    team = ["pkmn" + str(i + 1) for i in range(TEAM_SIZE + 1)]
    for member in team:
        pokemon_team_under_test.add_pokemon(member)
    assert pokemon_team_under_test.get_pokemon_roster() == team[:TEAM_SIZE]


def test_pokemon_team_add_pokemon_already_exists_should_not_add(
    pokemon_team_under_test,
):
    """Test adding already existing Pokémon to team"""
    team = ["pkmn1", "pkmn2", "pkmn3", "pkmn4", "pkmn5", "pkmn1"]
    expected_team = ["pkmn1", "pkmn2", "pkmn3", "pkmn4", "pkmn5"]
    for member in team:
        pokemon_team_under_test.add_pokemon(member)
    assert pokemon_team_under_test.get_pokemon_roster() == expected_team


def test_pokemon_usage_snapshot_get_set_pokemon_usage_happy_path(
    pokemon_usage_snapshot_under_test,
):
    """Test getting and setting Pokémon usage successfully"""
    pokemon_usage_snapshot_under_test.set_pokemon_usage("pkmn1", 50)
    assert pokemon_usage_snapshot_under_test.get_pokemon_usage("pkmn1") == 50


def test_pokemon_usage_snapshot_set_pokemon_usage_already_exists_should_not_set(
    pokemon_usage_snapshot_under_test,
):
    """Test setting Pokémon usage when Pokémon already exists"""
    pokemon_usage_snapshot_under_test.set_pokemon_usage("pkmn1", 50)
    pokemon_usage_snapshot_under_test.set_pokemon_usage("pkmn1", 70)
    assert pokemon_usage_snapshot_under_test.get_pokemon_usage("pkmn1") == 50


def test_pokemon_usage_snapshot_get_pokemon_usage_not_found_should_return_zero(
    pokemon_usage_snapshot_under_test,
):
    """Test getting non-existent Pokémon usage"""
    assert pokemon_usage_snapshot_under_test.get_pokemon_usage("pkmn1") == 0


def test_pokemon_usage_snapshot_get_set_pokemon_partner_usage_happy_path(
    pokemon_usage_snapshot_under_test,
):
    """Test getting and setting Pokémon partner usage successfully"""
    pokemon_usage_snapshot_under_test.set_pokemon_partner_usage("pkmn1", "partner1", 50)
    assert (
        pokemon_usage_snapshot_under_test.get_pokemon_partner_usage("pkmn1", "partner1")
        == 50
    )


def test_pokemon_usage_snapshot_set_pokemon_partner_usage_already_exists_should_not_set(
    pokemon_usage_snapshot_under_test,
):
    """Test setting Pokémon partner usage when partner already exists"""
    pokemon_usage_snapshot_under_test.set_pokemon_partner_usage("pkmn1", "partner1", 50)
    pokemon_usage_snapshot_under_test.set_pokemon_partner_usage("pkmn1", "partner1", 70)
    assert (
        pokemon_usage_snapshot_under_test.get_pokemon_partner_usage("pkmn1", "partner1")
        == 50
    )


def test_pokemon_usage_snapshot_get_pokemon_partner_usage_not_found_should_return_zero(
    pokemon_usage_snapshot_under_test,
):
    """Test getting non-existent Pokémon partner usage for Pokémon"""
    assert (
        pokemon_usage_snapshot_under_test.get_pokemon_partner_usage(
            "pkmn_non_existent", "no_partner"
        )
        == 0
    )


def test_pokemon_usage_snapshot_get_pokemon_partner_usage_partner_not_found_should_return_zero(
    pokemon_usage_snapshot_under_test,
):
    """Test getting non-existent Pokémon partner usage Pokémon partner"""
    pokemon_usage_snapshot_under_test.set_pokemon_partner_usage("pkmn1", "partner1", 50)
    assert (
        pokemon_usage_snapshot_under_test.get_pokemon_partner_usage(
            "pkmn1", "non_existent_partner"
        )
        == 0
    )


def test_pokemon_usage_snapshot_get_set_pokemon_average_rating_usage_happy_path(
    pokemon_usage_snapshot_under_test,
):
    """Test getting and setting Pokémon average rating successfully"""
    pokemon_usage_snapshot_under_test.set_pokemon_average_rating_usage("pkmn1", 50)
    assert (
        pokemon_usage_snapshot_under_test.get_pokemon_average_rating_usage("pkmn1")
        == 50
    )


def test_pokemon_usage_snapshot_set_pokemon_average_rating_usage_already_exists_should_not_set(
    pokemon_usage_snapshot_under_test,
):
    """Test setting already existing Pokémon average rating"""
    pokemon_usage_snapshot_under_test.set_pokemon_average_rating_usage("pkmn1", 50)
    pokemon_usage_snapshot_under_test.set_pokemon_average_rating_usage("pkmn1", 70)
    assert (
        pokemon_usage_snapshot_under_test.get_pokemon_average_rating_usage("pkmn1")
        == 50
    )


def test_pokemon_usage_snapshot_get_pokemon_average_rating_usage_not_found_should_return_zero(
    pokemon_usage_snapshot_under_test,
):
    """Test getting non-existent Pokémon average rating"""
    assert (
        pokemon_usage_snapshot_under_test.get_pokemon_average_rating_usage("pkmn1") == 0
    )
