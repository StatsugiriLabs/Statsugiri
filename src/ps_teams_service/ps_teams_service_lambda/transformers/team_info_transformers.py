from typing import List, Tuple
from data.team_info import TeamInfo
from data.get_team_response import GetTeamResponse
from data.get_teams_response import GetTeamsResponse
from utils.constants import COMPOSITE_DELIMITER


def transform_to_get_team_response(query_response: dict) -> GetTeamResponse:
    if query_response["Count"] == 0:
        return _get_empty_team_response()

    team_info = query_response["Items"][0]
    format_snapshot_date_composite = team_info["format_snapshot_date_composite"]["S"]
    format_id, snapshot_date = _parse_format_snapshot_date_composite_key(
        format_snapshot_date_composite
    )

    return GetTeamResponse(
        format_id,
        snapshot_date,
        TeamInfo(
            team_info["team_id"]["S"],
            team_info["pkmn_team"]["SS"],
            team_info["rating"]["N"],
            team_info["replay_id"]["S"],
            team_info["replay_upload_date"]["S"],
        ),
    )


def filter_and_transform_to_get_teams_response(
    query_response: dict, pkmn_to_filter: List[str]
) -> GetTeamsResponse:
    if query_response["Count"] == 0:
        return _get_empty_teams_response()

    sample_team_info = query_response["Items"][0]
    format_snapshot_date_composite = sample_team_info["format_snapshot_date_composite"][
        "S"
    ]
    format_id, snapshot_date = _parse_format_snapshot_date_composite_key(
        format_snapshot_date_composite
    )
    # Filter teams if provided
    team_info_filtered = (
        list(
            filter(
                lambda team: (
                    set(pkmn_to_filter).issubset(set(team["pkmn_team"]["SS"]))
                ),
                query_response["Items"],
            )
        )
        if pkmn_to_filter
        else query_response["Items"]
    )

    return GetTeamsResponse(
        len(team_info_filtered),
        format_id,
        snapshot_date,
        [
            TeamInfo(
                team_info["team_id"]["S"],
                team_info["pkmn_team"]["SS"],
                team_info["rating"]["N"],
                team_info["replay_id"]["S"],
                team_info["replay_upload_date"]["S"],
            )
            for team_info in team_info_filtered
        ],
    )


def _parse_format_snapshot_date_composite_key(
    format_snapshot_date_composite: str,
) -> Tuple[str, str]:
    format_snapshot_date_split = format_snapshot_date_composite.split(
        COMPOSITE_DELIMITER
    )
    format_id = format_snapshot_date_split[0]
    snapshot_date = format_snapshot_date_split[1]
    return (format_id, snapshot_date)


def _get_empty_team_response() -> GetTeamResponse:
    return GetTeamResponse("", "", TeamInfo("", [], 0, "", ""))


def _get_empty_teams_response() -> GetTeamsResponse:
    return GetTeamsResponse(0, "", "", [])
