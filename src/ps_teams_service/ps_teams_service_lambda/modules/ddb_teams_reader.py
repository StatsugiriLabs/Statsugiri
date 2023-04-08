from clients.teams_ddb_client import TeamsDdbClient
from transformers.team_info_transformers import (
    transform_to_get_team_response,
    filter_and_transform_to_get_teams_response,
)
from utils.serdes_utils import to_dict
from utils.base_logger import logger


class DdbTeamsReader:
    def __init__(self, teams_ddb_client: TeamsDdbClient):
        self.teams_ddb_client = teams_ddb_client

    def get_health_check(self) -> dict:
        """
        Return healthy ping
        :returns: health response
        """
        return {"health": "alive"}

    def get_team_by_id(self, team_id: str) -> dict:
        """
        Retrieve a team identified by team ID

        :param: team_id
        :returns: serialized GetTeamResponse
        """
        query_response = self.teams_ddb_client.query_team_by_id(team_id)
        get_team_response = transform_to_get_team_response(query_response)
        return to_dict(get_team_response)

    def get_teams_by_format_and_date(self, format: str, date: str) -> dict:
        """
        Retrieve teams from a format and date

        :param: format
        :param: date
        :returns: serialized GetTeamsResponse
        """
        query_response = self.teams_ddb_client.query_teams_by_format_and_date(
            format, date
        )
        get_teams_response = filter_and_transform_to_get_teams_response(
            query_response, ["arcanine"]
        )
        return to_dict(get_teams_response)
