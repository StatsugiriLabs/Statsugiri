import pytest
import os
import requests
import json
from modules.replay_handler import ReplayHandler
from modules.ladder_retriever import LadderRetriever
from data.ladder_user_info import LadderUserInfo
from unittest.mock import MagicMock
from bs4 import BeautifulSoup
from data.replay_info import ReplayInfo
from utils.errors import LadderNotFoundException

TEST_FORMAT = "test_format"
USER1_TEST_LOG = "test_log1"
USER1_UPLOAD_TIME = 1000000
NUM_USERS_TO_PULL = 1
USER1 = "user1"
RATING1 = 1001
USER1_REPLAY_ID = "test_format-1470016794"


@pytest.fixture(name="sample_user_replay_search_res_text")
def fixture_sample_user_replay_search_res_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_user_replay_search_res.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="mock_ladder_retriever")
def fixture_mock_ladder_retriever():
    return LadderRetriever()


@pytest.fixture(name="replay_handler_under_test")
def fixture_replay_handler_under_test(mock_ladder_retriever):
    return ReplayHandler(TEST_FORMAT, mock_ladder_retriever)


def init_mock_replay_res_content(
    id: str, format: str, log: str, uploadtime: int
) -> dict:
    return {"id": id, "format": format, "log": log, "uploadtime": uploadtime}


def init_mock_replay_json_response(
    status_code: int, replay_json: dict
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = json.dumps(replay_json, indent=2).encode("utf-8")
    return response


def init_expected_replay_info(
    id: str, username: str, rating: int, format: str, log: str, upload_time: int
) -> ReplayInfo:
    return ReplayInfo(id, username, rating, format, log, upload_time)


def test_extract_replays_happy_path(
    mocker,
    sample_user_replay_search_res_text,
    mock_ladder_retriever,
    replay_handler_under_test,
):
    mocker.patch(
        "modules.replay_handler.get_response_from_url",
        return_value=init_mock_replay_json_response(
            200,
            init_mock_replay_res_content(
                USER1_REPLAY_ID, TEST_FORMAT, USER1_TEST_LOG, USER1_UPLOAD_TIME
            ),
        ),
    )
    mocker.patch(
        "modules.replay_handler.get_soup_from_url",
        return_value=BeautifulSoup(sample_user_replay_search_res_text, "html.parser"),
    )
    mock_ladder_retriever.get_users = MagicMock(
        return_value=[LadderUserInfo(USER1, RATING1)]
    )

    replays = replay_handler_under_test.extract_replays(NUM_USERS_TO_PULL)
    assert replays == [
        init_expected_replay_info(
            USER1_REPLAY_ID,
            USER1,
            RATING1,
            TEST_FORMAT,
            USER1_TEST_LOG,
            USER1_UPLOAD_TIME,
        )
    ]


def test_extract_replays_no_replays_found_should_return_empty_list(
    mocker, mock_ladder_retriever, replay_handler_under_test
):
    mocker.patch(
        "modules.replay_handler.get_response_from_url",
        return_value=init_mock_replay_json_response(
            200,
            init_mock_replay_res_content(
                USER1_REPLAY_ID, TEST_FORMAT, USER1_TEST_LOG, USER1_UPLOAD_TIME
            ),
        ),
    )
    mocker.patch(
        "modules.replay_handler.get_soup_from_url",
        return_value=BeautifulSoup("no_replays_found_placeholder_html", "html.parser"),
    )
    mock_ladder_retriever.get_users = MagicMock(
        return_value=[LadderUserInfo(USER1, RATING1)]
    )

    replays = replay_handler_under_test.extract_replays(NUM_USERS_TO_PULL)
    assert replays == []


def test_extract_replays_key_not_found_should_raise_error(
    mocker,
    sample_user_replay_search_res_text,
    mock_ladder_retriever,
    replay_handler_under_test,
):
    mocker.patch(
        "modules.replay_handler.get_response_from_url",
        return_value=init_mock_replay_json_response(200, {}),
    )
    mocker.patch(
        "modules.replay_handler.get_soup_from_url",
        return_value=BeautifulSoup(sample_user_replay_search_res_text, "html.parser"),
    )
    mock_ladder_retriever.get_users = MagicMock(
        return_value=[LadderUserInfo(USER1, RATING1)]
    )

    with pytest.raises(KeyError):
        replay_handler_under_test.extract_replays(NUM_USERS_TO_PULL)


def test_extract_replays_ladder_not_found_should_raise_exception(
    mock_ladder_retriever, replay_handler_under_test
):
    mock_ladder_retriever.get_users = MagicMock(return_value=None)

    with pytest.raises(LadderNotFoundException):
        replay_handler_under_test.extract_replays(NUM_USERS_TO_PULL)
