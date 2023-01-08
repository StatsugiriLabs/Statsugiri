import pytest
from clients.ps_replay_extraction_client import PsReplayExtractionClient
from modules.replay_extractor import ReplayExtractor
from modules.ladder_retriever import LadderRetriever
from data.replay_info import ReplayInfo
from data.replay_snapshot import ReplaySnapshot
from data.ps_ingest_config import PsIngestConfig
from unittest.mock import MagicMock

REPLAY_ID = "id"
USERNAME = "user"
RATING = 1000
FORMAT = "test_format"
LOG = "test_log"
PKMN_TEAM = ["a", "b", "c"]
REPLAY_UPLOAD_DATE = "2022-01-04"
SNAPSHOT_DATE = "2022-01-05"
INGEST_CONFIG = PsIngestConfig(SNAPSHOT_DATE, FORMAT, 1)


@pytest.fixture(name="mock_ladder_retriever")
def fixture_mock_ladder_retriever():
    return LadderRetriever()


@pytest.fixture(name="mock_replay_extractor")
def fixture_mock_replay_extractor(mock_ladder_retriever):
    return ReplayExtractor(mock_ladder_retriever, INGEST_CONFIG)


@pytest.fixture(name="ps_replay_extraction_client_under_test")
def fixture_ps_replay_extraction_client_under_test(mock_replay_extractor):
    return PsReplayExtractionClient(mock_replay_extractor)


def init_expected_snapshot():
    return ReplaySnapshot(
        SNAPSHOT_DATE,
        FORMAT,
        [ReplayInfo(REPLAY_ID, USERNAME, RATING, FORMAT, LOG, REPLAY_UPLOAD_DATE)],
    )


def test_process_happy_path(
    ps_replay_extraction_client_under_test, mock_replay_extractor
):
    mock_replay_extractor.get_replay_snapshot = MagicMock(
        return_value=ReplaySnapshot(
            SNAPSHOT_DATE,
            FORMAT,
            [ReplayInfo(REPLAY_ID, USERNAME, RATING, FORMAT, LOG, REPLAY_UPLOAD_DATE)],
        )
    )
    snapshot = ps_replay_extraction_client_under_test.process()
    assert snapshot == init_expected_snapshot()
