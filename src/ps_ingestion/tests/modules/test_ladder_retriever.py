import pytest
import os
from modules.ladder_retriever import LadderRetriever
from data.ladder_user_info import LadderUserInfo
from bs4 import BeautifulSoup


@pytest.fixture(name="ladder_retriever_under_test")
def fixture_ladder_retriever_under_test():
    return LadderRetriever()


@pytest.fixture(name="sample_ladder_res_text")
def fixture_sample_ladder_res_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_ladder_res.txt"),
        encoding="utf-8",
    ).read()


def init_expected_ladder_user_info():
    user_infos = [("test1", 2005), ("test2", 2004), ("test3", 2003)]
    return [LadderUserInfo(user_info[0], user_info[1]) for user_info in user_infos]


def test_get_users_happy_path(
    mocker, ladder_retriever_under_test, sample_ladder_res_text
):
    mocker.patch(
        "modules.ladder_retriever.get_soup_from_url",
        return_value=BeautifulSoup(sample_ladder_res_text, "html.parser"),
    )

    users = ladder_retriever_under_test.get_users("test_format")
    assert users == init_expected_ladder_user_info()
