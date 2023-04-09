import pytest
import boto3
from unittest.mock import MagicMock
from clients.teams_ddb_client import TeamsDdbClient

TEST_TABLE_NAME = "TABLE_NAME"
TEST_TEAM_ID = "TEAM_ID"
TEST_FORMAT = "TEST_FORMAT"
TEST_DATE = "TEST_DATE"


@pytest.fixture(name="mock_ddb_client")
def fixture_mock_ddb_client():
    return boto3.client("dynamodb", region_name="us-east-1")


@pytest.fixture(name="teams_ddb_client_under_test")
def fixture_teams_ddb_client_under_test(mock_ddb_client):
    return TeamsDdbClient(mock_ddb_client, TEST_TABLE_NAME)


def init_mock_query_team_by_id_response():
    return {
        "Items": [
            {
                "team": {
                    "team_id": "545c4653-e471-460d-b56d-7b426b07c3da",
                    "format_snapshot_date_composite": "gen9vgc2023series2#2023-04-09",
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
        ]
    }


def init_mock_query_teams_by_format_and_date_response():
    return {
        "Items": [
            {
                "team": {
                    "team_id": "12345",
                    "format_snapshot_date_composite": "gen9vgc2023series2#2023-04-09",
                    "format_id": "gen9vgc2023series2",
                    "pkmn_team": [
                        "arcanine",
                        "baxcalibur",
                        "flutter mane",
                        "garganacl",
                        "iron hands",
                        "meowscarada",
                    ],
                    "rating": "1736",
                    "replay_id": "gen9vgc2023series2-12345",
                    "replay_upload_date": "2023-03-16",
                }
            },
            {
                "team": {
                    "team_id": "12346",
                    "format_snapshot_date_composite": "gen9vgc2023series2#2023-04-09",
                    "format_id": "gen9vgc2023series2",
                    "pkmn_team": [
                        "amoonguss",
                        "arcanine",
                        "corviknight",
                        "flutter mane",
                        "garchomp",
                        "tyranitar",
                    ],
                    "rating": "1736",
                    "replay_id": "gen9vgc2023series2-12346",
                    "replay_upload_date": "2023-03-16",
                }
            },
        ]
    }


def test_query_team_by_id_happy_path(teams_ddb_client_under_test, mock_ddb_client):
    mock_ddb_client.query = MagicMock(
        return_value=init_mock_query_team_by_id_response()
    )
    response = teams_ddb_client_under_test.query_team_by_id(TEST_TEAM_ID)
    assert response == init_mock_query_team_by_id_response()


def test_query_teams_by_format_and_date_happy_path(
    teams_ddb_client_under_test, mock_ddb_client
):
    mock_ddb_client.query = MagicMock(
        return_value=init_mock_query_teams_by_format_and_date_response()
    )
    response = teams_ddb_client_under_test.query_teams_by_format_and_date(
        TEST_FORMAT, TEST_DATE
    )
    assert response == init_mock_query_teams_by_format_and_date_response()
