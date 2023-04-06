from utils.errors import DdbTeamsReadException
from utils.constants import PAGINATION_LIMIT


class TeamsDdbClient:
    def __init__(self, ddb_client: any, table_name: str):
        self.ddb_client = ddb_client
        self.table_name = table_name

    def query_team_by_id(self, team_id: str) -> dict:
        """
        Query by team_id primary key

        :param: team_id
        :returns: query response
        """
        try:
            response = self.ddb_client.query(
                TableName=self.table_name,
                KeyConditionExpression="team_id = :team_id",
                ExpressionAttributeValues={":team_id": {"S": team_id}},
            )
            return response
        except Exception as e:
            raise DdbTeamsReadException(
                "Unable to query team by ID from DDB table for {team_id}: {err}".format(
                    team_id=team_id, err=str(e)
                )
            )

    def scan_teams(self) -> dict:
        # TODO: Implement query param flag for pkmn
        # TODO: Implement pagination
        try:
            response = self.ddb_client.scan(
                TableName=self.table_name, Limit=PAGINATION_LIMIT
            )
            print(response)
            return response
        except Exception as e:
            raise DdbTeamsReadException(
                "Unable to query team by ID from DDB table for scan: {err}".format(
                    err=str(e)
                )
            )

    def query_teams_by_format(self, format: str) -> dict:
        # TODO: Implement query param flag for pkmn
        # TODO: Implement pagination
        try:
            response = self.ddb_client.query(
                TableName=self.table_name,
                IndexName="formatIdIndex",
                KeyConditionExpression="format_id = :format_id",
                ExpressionAttributeValues={":format_id": {"S": format}},
                Limit=PAGINATION_LIMIT,
            )
            print(response)
            return response
        except Exception as e:
            raise DdbTeamsReadException(
                "Unable to query team by '{format}' format from DDB table: {err}".format(
                    format=format, err=str(e)
                )
            )

    def query_teams_by_format_and_date(self, format: str, date: str) -> dict:
        # TODO: Implement query param flag for pkmn
        # TODO: Implement pagination
        return {}
