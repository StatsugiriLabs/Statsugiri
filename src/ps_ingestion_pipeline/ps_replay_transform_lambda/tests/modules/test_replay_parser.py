import pytest
import os
from modules.replay_parser import ReplayParser

GENERIC_USER = "Bruce_poke"
GENERIC_TEAM = [
    "Zacian",
    "Lapras",
    "Thundurus",
    "Landorus-Therian",
    "Urshifu",
    "Incineroar",
]
INCOMPLETE_USER = "babiri_tester"
INCOMPLETE_TEAM = ["Groudon", "Yveltal", "Incineroar", "Regieleki", "pkmn4", "pkmn5"]
STRANGE_CHARS_USER = "SAHAbatgomba"
STRANGE_CHARS_TEAM = [
    "Armarouge",
    "Mimikyu",
    "Gholdengo",
    "Murkrow",
    "Torkoal",
    "Azumarill",
]
MAUSHOLD_USER = "iron ball ttar"
MAUSHOLD_TEAM = [
    "Flutter Mane",
    "Maushold",
    "Gholdengo",
    "Kingambit",
    "Volcarona",
    "Tauros-Paldea-Aqua",
]
SPACES_USER = "Leef2"
SPACES_TEAM = [
    "Roaring Moon",
    "Slither Wing",
    "Flutter Mane",
    "Torkoal",
    "Iron Hands",
    "Iron Bundle",
]


@pytest.fixture(name="sample_replay_log_generic_text")
def fixture_sample_replay_log_generic_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_replay_log_generic.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_replay_log_incomplete_team_text")
def fixture_sample_replay_log_incomplete_team_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_replay_log_incomplete_team.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_replay_log_strange_chars_text")
def fixture_sample_replay_log_strange_chars_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_replay_log_strange_chars.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_replay_log_spaces_text")
def fixture_sample_replay_log_spaces_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_replay_log_spaces.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="replay_parser_under_test")
def fixture_replay_parser_under_test():
    return ReplayParser()


def test_replay_parser_parse_team_happy_path(
    sample_replay_log_generic_text, replay_parser_under_test
):
    team = replay_parser_under_test.parse_team(
        GENERIC_USER, sample_replay_log_generic_text
    )
    assert team == GENERIC_TEAM


def test_replay_parser_parse_team_incomplete_team(
    sample_replay_log_incomplete_team_text, replay_parser_under_test
):
    team = replay_parser_under_test.parse_team(
        INCOMPLETE_USER, sample_replay_log_incomplete_team_text
    )
    assert team == INCOMPLETE_TEAM


def test_replay_parser_parse_team_maushold_team(
    sample_replay_log_spaces_text, replay_parser_under_test
):
    team = replay_parser_under_test.parse_team(
        MAUSHOLD_USER, sample_replay_log_spaces_text
    )
    assert team == MAUSHOLD_TEAM


def test_replay_parser_parse_team_spaces_team(
    sample_replay_log_spaces_text, replay_parser_under_test
):
    team = replay_parser_under_test.parse_team(
        SPACES_USER, sample_replay_log_spaces_text
    )
    assert team == SPACES_TEAM
