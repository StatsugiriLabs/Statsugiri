import pytest
import boto3
from unittest.mock import MagicMock
from transformers.team_info_transformers import (
    transform_to_get_team_response,
    filter_and_transform_to_get_teams_response,
)
from data.get_team_response import GetTeamResponse
from data.get_teams_response import GetTeamsResponse
from data.team_info import TeamInfo

TEST_TEAM_ID = "1234"
TEST_SNAPSHOT_DATE = "2023-04-03"
TEST_FORMAT_ID = "TEST_FORMAT"
TEST_SNAPSHOT_DATE_COMPOSITE = TEST_FORMAT_ID + "#" + TEST_SNAPSHOT_DATE
TEST_PKMN_TEAM = ["a", "b", "c", "d", "e", "f"]
TEST_RATING = 1602
TEST_REPLAY_ID = "REPLAY_ID"
TEST_REPLAY_UPLOAD_DATE = "REPLAY_UPLOAD_DATE"


def init_mock_transform_to_get_team_response_query_response():
    return {
        "Count": 1,
        "Items": [
            {
                "team_id": {"S": TEST_TEAM_ID},
                "format_snapshot_date_composite": {"S": TEST_SNAPSHOT_DATE_COMPOSITE},
                "pkmn_team": {"SS": TEST_PKMN_TEAM},
                "rating": {"N": TEST_RATING},
                "replay_id": {"S": TEST_REPLAY_ID},
                "replay_upload_date": {"S": TEST_REPLAY_UPLOAD_DATE},
            }
        ],
    }


def init_mock_filter_and_transform_to_get_teams_happy_path_response():
    return {
        "Count": 3,
        "Items": [
            {
                "team_id": {"S": "1"},
                "format_snapshot_date_composite": {"S": TEST_SNAPSHOT_DATE_COMPOSITE},
                "pkmn_team": {"SS": ["a", "b", "c", "d"]},
                "rating": {"N": 1003},
                "replay_id": {"S": "1"},
                "replay_upload_date": {"S": TEST_REPLAY_UPLOAD_DATE},
            },
            {
                "team_id": {"S": "2"},
                "format_snapshot_date_composite": {"S": TEST_SNAPSHOT_DATE_COMPOSITE},
                "pkmn_team": {"SS": ["a", "b", "c", "e"]},
                "rating": {"N": 1002},
                "replay_id": {"S": "2"},
                "replay_upload_date": {"S": TEST_REPLAY_UPLOAD_DATE},
            },
            {
                "team_id": {"S": "3"},
                "format_snapshot_date_composite": {"S": TEST_SNAPSHOT_DATE_COMPOSITE},
                "pkmn_team": {"SS": ["a", "b", "g", "h"]},
                "rating": {"N": 1001},
                "replay_id": {"S": "3"},
                "replay_upload_date": {"S": TEST_REPLAY_UPLOAD_DATE},
            },
        ],
    }


def init_mock_filter_and_transform_to_get_teams_c_filtered_response():
    return {
        "Count": 2,
        "Items": [
            {
                "team_id": {"S": "1"},
                "format_snapshot_date_composite": {"S": TEST_SNAPSHOT_DATE_COMPOSITE},
                "pkmn_team": {"SS": ["a", "b", "c", "d"]},
                "rating": {"N": 1003},
                "replay_id": {"S": "1"},
                "replay_upload_date": {"S": TEST_REPLAY_UPLOAD_DATE},
            },
            {
                "team_id": {"S": "2"},
                "format_snapshot_date_composite": {"S": TEST_SNAPSHOT_DATE_COMPOSITE},
                "pkmn_team": {"SS": ["a", "b", "c", "e"]},
                "rating": {"N": 1002},
                "replay_id": {"S": "2"},
                "replay_upload_date": {"S": TEST_REPLAY_UPLOAD_DATE},
            },
        ],
    }


def init_mock_get_teams_response_happy_path():
    return GetTeamsResponse(
        3,
        TEST_FORMAT_ID,
        TEST_SNAPSHOT_DATE,
        [
            TeamInfo("1", ["a", "b", "c", "d"], 1003, "1", TEST_REPLAY_UPLOAD_DATE),
            TeamInfo("2", ["a", "b", "c", "e"], 1002, "2", TEST_REPLAY_UPLOAD_DATE),
            TeamInfo("3", ["a", "b", "g", "h"], 1001, "3", TEST_REPLAY_UPLOAD_DATE),
        ],
    )


def init_mock_get_teams_response_c_filtered():
    return GetTeamsResponse(
        2,
        TEST_FORMAT_ID,
        TEST_SNAPSHOT_DATE,
        [
            TeamInfo("1", ["a", "b", "c", "d"], 1003, "1", TEST_REPLAY_UPLOAD_DATE),
            TeamInfo("2", ["a", "b", "c", "e"], 1002, "2", TEST_REPLAY_UPLOAD_DATE),
        ],
    )


def init_empty_count_response():
    return {"Count": 0}


def init_mock_get_team_response():
    return GetTeamResponse(
        TEST_FORMAT_ID,
        TEST_SNAPSHOT_DATE,
        TeamInfo(
            TEST_TEAM_ID,
            TEST_PKMN_TEAM,
            TEST_RATING,
            TEST_REPLAY_ID,
            TEST_REPLAY_UPLOAD_DATE,
        ),
    )


def init_mock_get_empty_team_response() -> GetTeamResponse:
    return GetTeamResponse("", "", TeamInfo("", [], 0, "", ""))


def init_mock_get_empty_teams_response() -> GetTeamsResponse:
    return GetTeamsResponse(0, "", "", [])


def test_transform_to_get_team_response_happy_path():
    response = transform_to_get_team_response(
        init_mock_transform_to_get_team_response_query_response()
    )
    assert response == init_mock_get_team_response()


def test_transform_to_get_team_response_empty_count_should_return_empty_team_response():
    response = transform_to_get_team_response(init_empty_count_response())
    assert response == init_mock_get_empty_team_response()


def test_filter_and_transform_to_get_teams_response_happy_path():
    response = filter_and_transform_to_get_teams_response(
        init_mock_filter_and_transform_to_get_teams_happy_path_response(), []
    )
    assert response == init_mock_get_teams_response_happy_path()


def test_filter_and_transform_to_get_teams_response_c_filtered():
    response = filter_and_transform_to_get_teams_response(
        init_mock_filter_and_transform_to_get_teams_c_filtered_response(), ["c"]
    )
    assert response == init_mock_get_teams_response_c_filtered()
