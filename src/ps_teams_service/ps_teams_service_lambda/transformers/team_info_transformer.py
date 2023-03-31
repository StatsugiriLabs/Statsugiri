from data.team_info import TeamInfo
from data.get_team_response import GetTeamResponse


def transform_get_team_by_id_to_response(query_response: dict) -> GetTeamResponse:
    if query_response["Count"] == 0:
        return GetTeamResponse(getEmptyTeamInfo())

    team_info = query_response["Items"][0]
    return GetTeamResponse(
        TeamInfo(
            team_info["team_id"]["S"],
            team_info["snapshot_date"]["S"],
            team_info["format_id"]["S"],
            team_info["pkmn_team"]["SS"],
            team_info["rating"]["N"],
            team_info["replay_id"]["S"],
            team_info["replay_upload_date"]["S"],
        )
    )


def getEmptyTeamInfo():
    return TeamInfo("", "", "", [], 0, "", "")
