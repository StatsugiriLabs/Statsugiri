from clients.teams_ddb_client import TeamsDdbClient
from transformers.team_info_transformer import transform_get_team_by_id_to_response
from utils.errors import DdbTeamsReadException
from utils.serdes_utils import to_dict


class DdbTeamsReader:
    def __init__(self, teams_ddb_client: TeamsDdbClient):
        self.teams_ddb_client = teams_ddb_client

    def get_health_check(self) -> dict:
        """
        Return 200 status code
        :returns: OK response
        """
        return {"statusCode": 200}

    def get_team_by_id(self, team_id: str) -> dict:
        """
        Retrieve a team identified by team ID

        :param: team_id
        :returns: serialized GetTeamsResponse
        """
        try:
            query_response = self.teams_ddb_client.query_team_by_id(team_id)
            get_team_response = transform_get_team_by_id_to_response(query_response)
            return to_dict(get_team_response)
        except Exception as e:
            raise DdbTeamsReadException(
                "Error reading from table: {err}".format(err=str(e))
            )
