import pytest
from constants import *
from data_extractor import *
import os

TEST_FORMATS = ["gen8vgc2021series10", "ou"]
NUM_TEAMS_TO_RETURN = 100
NUM_USERS_TO_SEARCH = 10

@pytest.fixture
def data_extractor_under_test():
    return DataExtractor(TEST_FORMATS, NUM_TEAMS_TO_RETURN)


@pytest.fixture
def sample_ladder_res_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(os.path.join(__location__, "assets/sample_ladder_res_text.txt")).read()

def test_get_ladder_rankings_happy_path(
    requests_mock, sample_ladder_res_text, data_extractor_under_test
):
    requests_mock.get(
        "https://pokemonshowdown.com/ladder/gen8vgc2021series10",
        text=sample_ladder_res_text,
    )
    users = data_extractor_under_test.get_ladder_users_and_ratings(
        "gen8vgc2021series10", NUM_USERS_TO_SEARCH
    )
    assert users == [
        ("y2ufjjkdkkdkd", 1639),
        ("wangjijiaoyu", 1638),
        ("Mara Martinez", 1637),
        ("JerryProduction", 1636),
        ("Ultra2018", 1636),
        ("GeorgeClooneyVgc", 1630),
        ("franpaolo", 1627),
        ("kakakataomoi", 1624),
        ("Kyodai Funseki", 1622),
        ("Snow07black", 1617),
    ]

def test_get_ladder_rankings_unavailable_format_should_raise_value_error(
    data_extractor_under_test
):
    with pytest.raises(ValueError, match="Format is unavailable"):
        data_extractor_under_test.get_ladder_users_and_ratings(
            "not_a_real_format", NUM_USERS_TO_SEARCH
        )

def test_get_ladder_rankings_greater_than_max_users_should_raise_value_error(
    data_extractor_under_test
):
    with pytest.raises(ValueError, match=r'Maximum number of users is \d+, \d+ was requested'):
        data_extractor_under_test.get_ladder_users_and_ratings(
            "gen8vgc2021series10", MAX_USERS + 1
        )
