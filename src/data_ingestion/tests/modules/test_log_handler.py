"""Unit tests for `LogHandler` class"""
import os
import json
import pytest
from modules.log_handler import LogHandler


@pytest.fixture(name="log_handler_under_test")
def fixture_log_handler(sample_replay_data_json):
    """Initialize log handler for tests"""
    log_handler = LogHandler()
    log_handler.feed_log(sample_replay_data_json)
    return log_handler


@pytest.fixture(name="sample_replay_data_json")
def fixture_sample_replay_data_json():
    """Read sample replay data JSON response for mocking GET request"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return json.loads(
        open(
            os.path.join(__location__, "../assets/sample_replay_data.json"),
            encoding="utf-8",
        ).read()
    )


@pytest.fixture(name="sample_cleaned_replay_data_json")
def fixture_sample_cleaned_replay_data_json():
    """Read sample cleaned replay data JSON response for mocking GET request"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return json.loads(
        open(
            os.path.join(__location__, "../assets/sample_cleaned_replay_data.json"),
            encoding="utf-8",
        ).read()
    )


@pytest.fixture(name="sample_replay_data_four_pkmn_json")
def fixture_sample_replay_data_four_pkmn_json():
    """Read replay data JSON response with 4 only Pokémon for mocking GET request"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return json.loads(
        open(
            os.path.join(__location__, "../assets/sample_replay_data_four_pkmn.json"),
            encoding="utf-8",
        ).read()
    )


def test_feed_log_happy_path(sample_cleaned_replay_data_json, log_handler_under_test):
    """Test sanitizing log from valid `replay_data`"""
    sanitized_log = log_handler_under_test.get_sanitized_log()
    assert sanitized_log == sample_cleaned_replay_data_json["log"]


def test_feed_log_no_log_field():
    """Test when `replay_data` has no 'log' field"""
    log_handler_under_test = LogHandler()
    assert not log_handler_under_test.feed_log({})


def test_parse_team_happy_path(sample_cleaned_replay_data_json, log_handler_under_test):
    """Test parsing teams from log given `p1` and `p2`"""
    p1_user = sample_cleaned_replay_data_json["p1"]
    p1_team = log_handler_under_test.parse_team(p1_user)
    p2_user = sample_cleaned_replay_data_json["p2"]
    p2_team = log_handler_under_test.parse_team(p2_user)
    assert p1_team == [
        "Zacian",
        "Lapras",
        "Thundurus",
        "Landorus-Therian",
        "Urshifu",
        "Incineroar",
    ]
    assert p2_team == [
        "Regieleki",
        "Calyrex-Shadow",
        "Indeedee-F",
        "Whimsicott",
        "Urshifu",
        "Rillaboom",
    ]


def test_parse_team_less_than_six_pkmn(
    sample_replay_data_four_pkmn_json, log_handler_under_test
):
    """Test parsing teams when log has less than 6 Pokémon present"""
    log_handler_under_test.feed_log(sample_replay_data_four_pkmn_json)
    team = log_handler_under_test.parse_team("babiri_tester")
    assert team == ["Groudon", "Yveltal", "Incineroar", "Regieleki"]


def test_parse_teams_team_invalid_user_should_return_empty(log_handler_under_test):
    """Test team parsing when user provided is an empty string"""
    assert log_handler_under_test.parse_team("") == []


def test_parse_teams_team_empty_log_should_return_empty():
    """Test team parsing when no log has been initialized"""
    # Initialize `log_handler` without populated `sanitized_log`
    log_handler_under_test = LogHandler()
    assert log_handler_under_test.parse_team("") == []


def test_parse_teams_team_player_not_found_should_return_empty(log_handler_under_test):
    """Test team parsing when player not found"""
    assert log_handler_under_test.parse_team("not_a_user") == []


def test_parse_teams_team_team_not_found_should_return_empty():
    """Test team parsing when team is not found"""
    log_handler_under_test = LogHandler()
    # Feed log with valid, parseable user without team
    log_handler_under_test.feed_log({"log": "|player|p1|user_without_team|"})
    assert log_handler_under_test.parse_team("user_without_team") == []
