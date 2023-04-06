from clients.teams_ddb_client import TeamsDdbClient
from typing import List
from utils.base_logger import logger
import uuid
from utils.constants import (
    SNAPSHOT_DATE_EVENT_ARG,
    FORMAT_ID_EVENT_ARG,
    TEAM_LIST_EVENT_ARG,
    PKMN_TEAM_EVENT_ARG,
    RATING_EVENT_ARG,
    ID_EVENT_ARG,
    REPLAY_UPLOAD_DATE_EVENT_ARG,
)
from utils.errors import DdbTeamsWriteException

TEAM_ID_DDB_KEY = "team_id"
FORMAT_SNAPSHOT_DATE_DDB_KEY = "format_snapshot_date_composite"
PKMN_TEAM_DDB_KEY = "pkmn_team"
REPLAY_ID_DDB_KEY = "replay_id"
REPLAY_UPLOAD_DATE_DDB_KEY = "replay_upload_date"
RATING_DDB_KEY = "rating"
COMPOSITE_DELIMIT = "#"


class DdbTeamsWriter:
    def __init__(self, teams_ddb_client: TeamsDdbClient):
        self.teams_ddb_client = teams_ddb_client

    def write(self, team_snapshot_payload: dict) -> bool:
        """
        Write team snapshot items to DynamoDB

        :param: teams_snapshot_payload
        :returns: success
        """
        snapshot_date = team_snapshot_payload[SNAPSHOT_DATE_EVENT_ARG]
        format_id = team_snapshot_payload[FORMAT_ID_EVENT_ARG]
        team_list = team_snapshot_payload[TEAM_LIST_EVENT_ARG]

        try:
            for team_info in team_list:
                team_id = str(uuid.uuid4())
                snapshot_date = snapshot_date
                lowercase_team_list = [
                    pkmn.lower() for pkmn in team_info[PKMN_TEAM_EVENT_ARG]
                ]

                team_item = {
                    TEAM_ID_DDB_KEY: {"S": team_id},
                    FORMAT_SNAPSHOT_DATE_DDB_KEY: {
                        "S": format_id + COMPOSITE_DELIMIT + snapshot_date
                    },
                    REPLAY_ID_DDB_KEY: {"S": team_info[ID_EVENT_ARG]},
                    PKMN_TEAM_DDB_KEY: {"SS": lowercase_team_list},
                    RATING_DDB_KEY: {"N": str(team_info[RATING_EVENT_ARG])},
                    REPLAY_UPLOAD_DATE_DDB_KEY: {
                        "S": team_info[REPLAY_UPLOAD_DATE_EVENT_ARG]
                    },
                }
                self.teams_ddb_client.put_item(team_item)
            return True
        except Exception as e:
            raise DdbTeamsWriteException(
                "Error writing to table: {err}".format(err=str(e))
            )
