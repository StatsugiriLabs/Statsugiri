import pytest
import os
from modules.replay_parser import ReplayParser
from data.replay_info import ReplayInfo
from data.team_snapshot_info import TeamSnapshotInfo
from typing import List

GENERIC_LOG_USER = "Bruce_poke"
INCOMPLETE_TEAM_LOG_USER = "babiri_tester"
MULTIPLE_FORMS_TEAM = [
    "Zacian",
    "Lapras",
    "Thundurus",
    "Landorus-Therian",
    "Urshifu",
    "Incineroar",
]
INCOMPLETE_TEAM = ["Groudon", "Yveltal", "Incineroar", "Regieleki", "pkmn4", "pkmn5"]
REPLAY_ID = 1
SNAPSHOT_DATE = "2022-01-05"
RATING = 1000
FORMAT = "test_format"
# UPLOAD_TIME should fall on same day as REPLAY_UPLOAD_TIME
REPLAY_UPLOAD_DATE_STR = "2022-01-04"
REPLAY_UPLOAD_TIME_TIMESTAMP = 1641313941


@pytest.fixture(name="replay_parser_under_test")
def fixture_replay_parser_under_test():
    return ReplayParser()


@pytest.fixture(name="sample_replay_log_generic_text")
def fixture_sample_replay_log_generic_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_replay_log_generic.txt"),
        encoding="utf-8",
    ).read()


@pytest.fixture(name="sample_replay_log_incomplete_team_text")
def fixture_sample_replay_log_incomplete_team_text():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "../assets/sample_replay_log_incomplete_team.txt"),
        encoding="utf-8",
    ).read()


def init_sample_replay_info(username: str, log: str):
    return ReplayInfo(
        REPLAY_ID, username, RATING, FORMAT, log, REPLAY_UPLOAD_TIME_TIMESTAMP
    )


def init_expected_teams_snapshot(teams: List[List[str]]):
    return [
        TeamSnapshotInfo(
            REPLAY_ID, team, SNAPSHOT_DATE, RATING, REPLAY_UPLOAD_DATE_STR, FORMAT
        )
        for team in teams
    ]


def test_transform_to_teams_snapshot_multiple_forms_happy_path(
    replay_parser_under_test, sample_replay_log_generic_text
):
    sample_replay_info_list = [
        init_sample_replay_info(GENERIC_LOG_USER, sample_replay_log_generic_text)
    ]

    snapshot = replay_parser_under_test.transform_to_teams_snapshot(
        sample_replay_info_list, SNAPSHOT_DATE
    )
    assert snapshot == init_expected_teams_snapshot([MULTIPLE_FORMS_TEAM])


def test_transform_to_teams_snapshot_incomplete_team(
    replay_parser_under_test, sample_replay_log_incomplete_team_text
):
    sample_replay_info_list = [
        init_sample_replay_info(
            INCOMPLETE_TEAM_LOG_USER, sample_replay_log_incomplete_team_text
        )
    ]

    snapshot = replay_parser_under_test.transform_to_teams_snapshot(
        sample_replay_info_list, SNAPSHOT_DATE
    )
    assert snapshot == init_expected_teams_snapshot([INCOMPLETE_TEAM])
