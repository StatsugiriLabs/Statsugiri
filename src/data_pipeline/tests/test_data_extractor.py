"""Unit tests for `DataExtractor` class"""
import os
import json
import pytest
from constants import MAX_USERS
from data_extractor import DataExtractor

TEST_FORMATS = ["gen8vgc2021series11"]
NUM_TEAMS_TO_RETURN = 100
NUM_USERS_TO_SEARCH = 10


@pytest.fixture(name="data_extractor_under_test")
def fixture_data_extractor():
    """Initialize data extractor for tests"""
    return DataExtractor(0, TEST_FORMATS, NUM_TEAMS_TO_RETURN)


@pytest.fixture(name="sample_ladder_res_text")
def fixture_sample_ladder_res_text():
    """Read sample ladder response text for mocking GET request"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "assets/sample_ladder_res_text.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_ladder_ToastNoButter_res_text")
def fixture_sample_ladder_ToastNoButter_res_text():
    """Read sample ladder response text for mocking GET request with only 'ToastNoButter' recorded"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "assets/sample_ladder_ToastNoButter_res_text.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_user_replays_res_text")
def fixture_sample_user_replays_res_text():
    """Read sample user's replays response text mocking GET request"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "assets/sample_user_replays_res_text.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_user_replays_ToastNoButter_res_text")
def fixture_sample_user_replays_ToastNoButter_res_text():
    """Read sample ladder response text for mocking GET request for 'ToastNoButter' user replays"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(
            __location__, "assets/sample_user_replays_ToastNoButter_res_text.txt"
        ),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_replay_data_ToastNoButter_json")
def fixture_sample_replay_data_ToastNoButter_json():
    """Read sample replay response JSON for mocking GET request for 'ToastNoButter'"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return json.loads(
        open(
            os.path.join(__location__, "assets/sample_replay_data_ToastNoButter.json"),
            encoding="utf-8",
        ).read()
    )


def test_get_ladder_users_and_ratings_happy_path(
    requests_mock, sample_ladder_res_text, data_extractor_under_test
):
    """Test user and ranking ladder retrieval"""
    requests_mock.get(
        "https://pokemonshowdown.com/ladder/gen8vgc2021series11",
        text=sample_ladder_res_text,
    )
    users = data_extractor_under_test.get_ladder_users_and_ratings(
        "gen8vgc2021series11", NUM_USERS_TO_SEARCH
    )
    assert users == [
        ("super sweett", 1904),
        ("ToastNoButter", 1874),
        ("suncha", 1841),
        ("2sexy4vgc", 1837),
        ("mikebosc", 1824),
        ("MaidenMicaiah", 1810),
        ("Saudiarabia3", 1807),
        ("Tt08", 1785),
        ("Poiserd", 1776),
        ("bblgo", 1776),
    ]


def test_get_ladder_users_and_ratings_unavailable_format_should_raise_value_error(
    data_extractor_under_test,
):
    """Test when unsupported format is provided"""
    with pytest.raises(ValueError, match=r"Format (.+) is unavailable"):
        data_extractor_under_test.get_ladder_users_and_ratings(
            "not_a_real_format", NUM_USERS_TO_SEARCH
        )


def test_get_ladder_users_and_ratings_greater_than_max_users_should_raise_value_error(
    data_extractor_under_test,
):
    """Test when number of users requested is greater than available users"""
    with pytest.raises(
        ValueError, match=r"Maximum number of users is \d+, \d+ was requested"
    ):
        data_extractor_under_test.get_ladder_users_and_ratings(
            "gen8vgc2021series11", MAX_USERS + 1
        )


def test_sanitize_user(data_extractor_under_test):
    """Test removing non-ASCII characters and spaces"""
    sanitized_user = data_extractor_under_test.sanitize_user("user test 中文")
    assert sanitized_user == "usertest"


def test_get_user_replay_ids_happy_path(
    requests_mock, sample_user_replays_res_text, data_extractor_under_test
):
    """Test user replay ID retrieval"""
    requests_mock.get(
        "https://replay.pokemonshowdown.com/search/?output=html&user=SayNoToSpachet",
        text=sample_user_replays_res_text,
    )
    replay_ids = data_extractor_under_test.get_user_replay_ids(
        "SayNoToSpachet", "gen8vgc2021series11"
    )
    assert replay_ids == [
        "gen8vgc2021series11-1468972576",
        "gen8vgc2021series11-1468427683",
        "gen8vgc2021series11-1466694825",
        "gen8vgc2021series11-1466507645",
        "gen8vgc2021series11-1466388772",
        "gen8vgc2021series11-1465712586",
        "gen8vgc2021series11-1463340788",
        "gen8vgc2021series11-1463175352",
    ]


# TODO: https://github.com/kelvinkoon/babiri_v2/issues/46
def test_extract_info_happy_path(
    mocker, sample_replay_data_ToastNoButter_json, data_extractor_under_test
):
    """Test extracting info cycle"""
    users = [("ToastNoButter", 1874)]
    replay_ids = [
        "gen8vgc2021series11-1483710801",
        "gen8vgc2021series11-1483657513",
        "gen8vgc2021series11-1482150610",
        "gen8vgc2021series11-1482135387",
        "gen8vgc2021series11-1481400639",
        "gen8vgc2021series11-1481391310",
        "gen8vgc2021series11-1481377054",
        "gen8vgc2021series11-1479481903",
        "gen8vgc2021series11-1479464786",
        "gen8vgc2021series11-1479462077",
        "gen8vgc2021series11-1479449630",
        "gen8vgc2021series11-1478902568",
        "gen8vgc2021series11-1478454710",
        "gen8vgc2021series11-1478308804",
        "gen8vgc2021series11-1478300602",
        "gen8vgc2021series11-1477763896",
        "gen8vgc2021series11-1477759413",
        "gen8vgc2021series11-1476414583",
        "gen8vgc2021series11-1476398026",
        "gen8vgc2021series11-1476395636",
        "gen8vgc2021series11-1476037573",
        "gen8vgc2021series11-1476035911",
        "gen8vgc2021series11-1476027554",
        "gen8vgc2021series11-1475507871",
        "gen8vgc2021series11-1475368059",
        "gen8vgc2021series11-1474886856",
        "gen8vgc2021series11-1474869237",
        "gen8vgc2021series11-1474865018",
        "gen8vgc2021series11-1474772915",
        "gen8vgc2021series11-1474761247",
        "gen8vgc2021series11-1474236147",
        "gen8vgc2021series11-1473569650",
        "gen8vgc2021series11-1472907115",
        "gen8vgc2021series11-1472826492",
        "gen8vgc2021series11-1472821150",
        "gen8vgc2021series11-1472815787",
        "gen8vgc2021series11-1472800139",
    ]
    team = [
        "Whimsicott",
        "Calyrex-Shadow",
        "Urshifu",
        "Tapu Lele",
        "Thundurus",
        "Chandelure",
    ]
    # Configure for one team
    data_extractor_under_test.set_num_teams(1)
    # Mock functions outside of module
    mocker.patch(
        "data_extractor.DataExtractor.get_ladder_users_and_ratings", return_value=users
    )
    mocker.patch(
        "data_extractor.DataExtractor.get_user_replay_ids", return_value=replay_ids
    )
    mocker.patch(
        "data_extractor.DataExtractor.get_replay_data",
        return_value=sample_replay_data_ToastNoButter_json,
    )
    mocker.patch("log_handler.LogHandler.feed_log", return_value=True)
    mocker.patch("log_handler.LogHandler.parse_team", return_value=team)
    # Take VGC format, which is the first in `TEST_FORMATS`
    data_extractor_under_test.extract_info(TEST_FORMATS[0])
    assert (
        data_extractor_under_test.get_parsed_user_replay_list()[0].get_pokemon_roster()
        == team
    )
