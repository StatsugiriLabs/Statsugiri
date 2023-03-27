from clients.teams_ddb_client import TeamsDdbClient
from typing import List
from utils.base_logger import logger
from utils.errors import DdbTeamsReadException

PK_DDB_KEY = "pk"
SK_DDB_KEY = "sk"
SNAPSHOT_DATE_DDB_KEY = "snapshot_date"
FORMAT_ID_DDB_KEY = "format_id"
PKMN_TEAM_DDB_KEY = "pkmn_team"
REPLAY_ID_DDB_KEY = "replay_id"
REPLAY_UPLOAD_DATE_DDB_KEY = "replay_upload_date"
RATING_DDB_KEY = "rating"

DATE_FIELD_PREFIX = "date"
PKMN_FIELD_PREFIX = "pkmn"
SK_DELIMITER = "#"


class DdbTeamsReader:
    def __init__(self, teams_ddb_client: TeamsDdbClient):
        self.teams_ddb_client = teams_ddb_client

    def get_team(self, team_id: str) -> bool:
        """
        Retrieve a team identified by ID

        :param: team_id
        :returns: success
        """
        try:
            # TODO: What does response obj look like?
            self.teams_ddb_client.query_team_by_id(team_id)
            # TODO: Transform to response
            return True
        except Exception as e:
            raise DdbTeamsReadException(
                "Error reading from table:{err}".format(err=str(e))
            )
