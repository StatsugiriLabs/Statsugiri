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

class DdbTeamsWriter:
    def __init__(self, teams_ddb_client: TeamsDdbClient):
        self.teams_ddb_client = teams_ddb_client

    def write(self, team_snapshot_payload: dict) -> bool:
        """
        Write team records to DynamoDB

        :param: teams_snapshot_payload
        :returns: success
        """
        snapshot_date = team_snapshot_payload[SNAPSHOT_DATE_EVENT_ARG]
        format_id = team_snapshot_payload[FORMAT_ID_EVENT_ARG]
        team_list = team_snapshot_payload[TEAM_LIST_EVENT_ARG]

        for team_info in team_list:
            pk_id = str(uuid.uuid4())
            date_field = DATE_FIELD_PREFIX + SK_DELIMITER + snapshot_date
            lowercase_team_list = [
                pkmn.lower() for pkmn in team_info[PKMN_TEAM_EVENT_ARG]
            ]

            # Write primary team item
            primary_team_item = {
                PK_DDB_KEY: {"S": pk_id},
                SK_DDB_KEY: {"S": date_field},
                SNAPSHOT_DATE_DDB_KEY: {"S": snapshot_date},
                FORMAT_ID_DDB_KEY: {"S": format_id},
                REPLAY_ID_DDB_KEY: {"S": team_info[ID_EVENT_ARG]},
                PKMN_TEAM_DDB_KEY: {"SS": lowercase_team_list},
                RATING_DDB_KEY: {"N": str(team_info[RATING_EVENT_ARG])},
                REPLAY_UPLOAD_DATE_DDB_KEY: {
                    "S": team_info[REPLAY_UPLOAD_DATE_EVENT_ARG]
                },
            }
            self.teams_ddb_client.put_item(primary_team_item)

            # Write pkmn_team items
            for pkmn in lowercase_team_list:
                pkmn_field = PKMN_FIELD_PREFIX + SK_DELIMITER + pkmn
                pkmn_team_item = {
                    PK_DDB_KEY: {"S": pk_id},
                    SK_DDB_KEY: {"S": pkmn_field},
                }
                self.teams_ddb_client.put_item(pkmn_team_item)

        return True
