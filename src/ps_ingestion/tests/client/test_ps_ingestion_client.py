import pytest
from client.ps_ingestion_client import PsIngestionClient
from modules.replay_handler import ReplayHandler
from modules.replay_parser import ReplayParser
from modules.ladder_retriever import LadderRetriever
from data.replay_info import ReplayInfo
from data.team_snapshot_info import TeamSnapshotInfo
from data.ingest_data_info import IngestDataInfo
from unittest.mock import MagicMock

REPLAY_ID = "id"
USERNAME = "user"
RATING = 1000
FORMAT = "test_format"
LOG = "test_log"
PKMN_TEAM = ["a", "b", "c"]
# UPLOAD_TIME should fall on same day as REPLAY_UPLOAD_TIME
REPLAY_UPLOAD_DATE_STR = "2022-01-04"
REPLAY_UPLOAD_TIME_TIMESTAMP = 1641313941
SNAPSHOT_DATE = "2022-01-05"
INGEST_DATA = IngestDataInfo(SNAPSHOT_DATE, 1)


@pytest.fixture(name="mock_ladder_retriever")
def fixture_mock_ladder_retriever():
    return LadderRetriever()


@pytest.fixture(name="mock_replay_parser")
def fixture_mock_replay_parser():
    return ReplayParser()


@pytest.fixture(name="mock_replay_handler")
def fixture_mock_replay_handler(mock_ladder_retriever):
    return ReplayHandler(FORMAT, mock_ladder_retriever)


@pytest.fixture(name="ps_ingestion_client_under_test")
def fixture_ps_ingestion_client_under_test(mock_replay_handler, mock_replay_parser):
    return PsIngestionClient(mock_replay_handler, mock_replay_parser)


def init_expected_snapshot():
    return [
        TeamSnapshotInfo(
            REPLAY_ID, PKMN_TEAM, SNAPSHOT_DATE, RATING, REPLAY_UPLOAD_DATE_STR, FORMAT
        )
    ]


def test_process_happy_path(
    ps_ingestion_client_under_test, mock_replay_handler, mock_replay_parser
):
    mock_replay_handler.extract_replays = MagicMock(
        return_value=[
            ReplayInfo(
                REPLAY_ID, USERNAME, RATING, FORMAT, LOG, REPLAY_UPLOAD_TIME_TIMESTAMP
            )
        ]
    )
    mock_replay_parser.transform_to_teams_snapshot = MagicMock(
        return_value=[
            TeamSnapshotInfo(
                REPLAY_ID,
                PKMN_TEAM,
                SNAPSHOT_DATE,
                RATING,
                REPLAY_UPLOAD_DATE_STR,
                FORMAT,
            )
        ]
    )
    snapshot = ps_ingestion_client_under_test.process(INGEST_DATA)
    assert snapshot == init_expected_snapshot()
