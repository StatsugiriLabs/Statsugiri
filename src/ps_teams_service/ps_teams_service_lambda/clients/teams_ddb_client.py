from mypy_boto3_dynamodb import DynamoDBClient
from utils.errors import DdbTeamsReadException


class TeamsDdbClient:
    def __init__(self, ddb_client: DynamoDBClient, table_name: str):
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
