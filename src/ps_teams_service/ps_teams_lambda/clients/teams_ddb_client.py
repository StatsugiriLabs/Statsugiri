from mypy_boto3_dynamodb import DynamoDBClient
from utils.errors import DdbTeamsReadException
import time


class TeamsDdbClient:
    def __init__(self, ddb_client: DynamoDBClient, table_name: str):
        self.ddb_client = ddb_client
        self.table_name = table_name

    def query_team_by_id(self, team_id: str) -> None:
        """
        TODO

        :param: item
        :returns: None
        """
        try:
            response = self.ddb_client.get_item(
                TableName=self.table_name, Key={"team_id": {"S": team_id}}
            )
            print(response)
        except Exception as e:
            raise DdbTeamsReadException(
                "Unable to read from DDB table for {team_id}: {err}".format(
                    team_id=team_id, err=str(e)
                )
            )
