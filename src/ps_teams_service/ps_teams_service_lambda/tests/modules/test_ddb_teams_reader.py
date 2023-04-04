import pytest
import boto3
from unittest.mock import MagicMock
from clients.teams_ddb_client import TeamsDdbClient
from modules.ddb_teams_reader import DdbTeamsReader

TEST_TABLE_NAME = "TABLE_NAME"
TEST_TEAM_ID = "TEAM_ID"


@pytest.fixture(name="mock_teams_ddb_client")
def fixture_mock_teams_ddb_client():
    return TeamsDdbClient(None, TEST_TABLE_NAME)


@pytest.fixture(name="ddb_teams_reader_under_test")
def fixture_ddb_teams_reader_under_test(mock_teams_ddb_client):
    return DdbTeamsReader(mock_teams_ddb_client)


def init_mock_response():
    return {
        "team": {
            "team_id": "545c4653-e471-460d-b56d-7b426b07c3da",
            "snapshot_date": "2023-04-03",
            "format_id": "gen9vgc2023series2",
            "pkmn_team": [
                "baxcalibur",
                "brute bonnet",
                "gholdengo",
                "mimikyu",
                "palafin",
                "pelipper",
            ],
            "rating": "1732",
            "replay_id": "gen9vgc2023series2-1823224855",
            "replay_upload_date": "2023-03-16",
        }
    }


def test_get_health_check_happy_path(ddb_teams_reader_under_test):
    response = ddb_teams_reader_under_test.get_health_check()
    assert response == {"health": "alive"}
