import pytest
from lambda_typing.types import LambdaDict
from unittest.mock import MagicMock
from clients.ps_replay_transform_client import PsReplayTransformClient
from modules.replay_parser import ReplayParser
from data.team_snapshot import TeamSnapshot
from data.team_info import TeamInfo
from utils.constants import (
    SNAPSHOT_DATE_EVENT_ARG,
    FORMAT_ID_EVENT_ARG,
    REPLAY_LIST_EVENT_ARG,
    REPLAY_ID_EVENT_ARG,
    REPLAY_USERNAME_EVENT_ARG,
    REPLAY_RATING_EVENT_ARG,
    REPLAY_LOG_EVENT_ARG,
    REPLAY_UPLOAD_DATE_EVENT_ARG,
)

TEST_SNAPSHOT_DATE = "2022-01-02"
TEST_FORMAT_ID = "test_format"
TEST_REPLAY_USERNAME = "user"
TEST_REPLAY_LOG = "log"
TEST_REPLAY_ID = "id"
TEST_TEAM = ["a", "b", "c", "d", "e", "f"]
TEST_RATING = 1000
TEST_UPLOAD_DATE = "2022-01-01"


@pytest.fixture(name="mock_replay_parser")
def fixture_mock_replay_parser():
    return ReplayParser()


@pytest.fixture(name="ps_replay_transform_client_under_test")
def fixture_ps_replay_transform_client_under_test(mock_replay_parser):
    return PsReplayTransformClient(mock_replay_parser)


def init_test_lambda_event():
    return {
        SNAPSHOT_DATE_EVENT_ARG: TEST_SNAPSHOT_DATE,
        FORMAT_ID_EVENT_ARG: TEST_FORMAT_ID,
        REPLAY_LIST_EVENT_ARG: [
            {
                REPLAY_USERNAME_EVENT_ARG: TEST_REPLAY_USERNAME,
                REPLAY_LOG_EVENT_ARG: TEST_REPLAY_LOG,
                REPLAY_ID_EVENT_ARG: TEST_REPLAY_ID,
                REPLAY_RATING_EVENT_ARG: TEST_RATING,
                REPLAY_UPLOAD_DATE_EVENT_ARG: TEST_UPLOAD_DATE,
            }
        ],
    }


def init_expected_snapshot():
    return TeamSnapshot(
        TEST_SNAPSHOT_DATE,
        TEST_FORMAT_ID,
        [TeamInfo(TEST_REPLAY_ID, TEST_TEAM, TEST_RATING, TEST_UPLOAD_DATE)],
    )


def test_process_happy_path(ps_replay_transform_client_under_test, mock_replay_parser):
    mock_replay_parser.parse_team = MagicMock(return_value=TEST_TEAM)
    snapshot = ps_replay_transform_client_under_test.transform(init_test_lambda_event())
    assert snapshot == init_expected_snapshot()
