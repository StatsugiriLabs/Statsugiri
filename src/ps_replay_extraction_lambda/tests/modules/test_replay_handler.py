import pytest
from unittest.mock import MagicMock
import os
import requests
import json
from bs4 import BeautifulSoup
from modules.replay_extractor import ReplayExtractor
from modules.ladder_retriever import LadderRetriever
from data.ladder_user_info import LadderUserInfo
from data.ps_ingest_config import PsIngestConfig
from data.replay_info import ReplayInfo
from data.replay_snapshot import ReplaySnapshot
from utils.errors import LadderNotFoundException

TEST_FORMAT = "test_format"
USER_TEST_LOG = "test_log"
USER_UPLOAD_TIME_TIMESTAMP = 1641035544
USER_UPLOAD_TIME_STR = "2022-01-01"
NUM_REPLAYS_TO_PULL = 1
USER = "user1"
RATING = 1001
USER_REPLAY_ID = "test_format-1470016794"
SNAPSHOT_DATE = "2022-01-02"


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


@pytest.fixture(name="replay_extractor_under_test")
def fixture_replay_extractor_under_test(mock_ladder_retriever):
    ingest_config = PsIngestConfig(SNAPSHOT_DATE, TEST_FORMAT, NUM_REPLAYS_TO_PULL)
    return ReplayExtractor(mock_ladder_retriever, ingest_config)


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


def test_get_replay_snapshot_happy_path(
    mocker,
    sample_user_replay_search_res_text,
    mock_ladder_retriever,
    replay_extractor_under_test,
):
    mocker.patch(
        "modules.replay_extractor.get_response_from_url",
        return_value=init_mock_replay_json_response(
            200,
            init_mock_replay_res_content(
                USER_REPLAY_ID, TEST_FORMAT, USER_TEST_LOG, USER_UPLOAD_TIME_TIMESTAMP
            ),
        ),
    )
    mock_ladder_retriever.get_users = MagicMock(
        return_value=[LadderUserInfo(USER, RATING)]
    )
    mocker.patch(
        "modules.replay_extractor.get_soup_from_url",
        return_value=BeautifulSoup(sample_user_replay_search_res_text, "html.parser"),
    )

    replays = replay_extractor_under_test.get_replay_snapshot()
    assert replays == ReplaySnapshot(
        SNAPSHOT_DATE,
        TEST_FORMAT,
        [
            init_expected_replay_info(
                USER_REPLAY_ID,
                USER,
                RATING,
                TEST_FORMAT,
                USER_TEST_LOG,
                USER_UPLOAD_TIME_STR,
            )
        ],
    )


def test_get_replay_snapshot_no_ladder_ladder_not_found(
    replay_extractor_under_test, mock_ladder_retriever
):
    mock_ladder_retriever.get_users = MagicMock(return_value=[])

    with pytest.raises(LadderNotFoundException):
        replay_extractor_under_test.get_replay_snapshot()


def test_get_replay_snapshot_recent_replay_exception_skip_replay(
    mocker,
    mock_ladder_retriever,
    replay_extractor_under_test,
):
    mocker.patch(
        "modules.replay_extractor.get_response_from_url",
        return_value=init_mock_replay_json_response(
            200,
            init_mock_replay_res_content(
                USER_REPLAY_ID, TEST_FORMAT, USER_TEST_LOG, USER_UPLOAD_TIME_TIMESTAMP
            ),
        ),
    )
    mock_ladder_retriever.get_users = MagicMock(
        return_value=[LadderUserInfo(USER, RATING)]
    )
    mocker.patch("modules.replay_extractor.get_soup_from_url", return_value=Exception)

    replays = replay_extractor_under_test.get_replay_snapshot()
    assert replays == ReplaySnapshot(SNAPSHOT_DATE, TEST_FORMAT, [])
