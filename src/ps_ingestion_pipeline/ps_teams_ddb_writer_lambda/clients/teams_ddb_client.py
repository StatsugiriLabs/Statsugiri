from mypy_boto3_dynamodb import DynamoDBClient
from utils.errors import DdbTeamsWriteException


class TeamsDdbClient:
    def __init__(self, ddb_client: DynamoDBClient, table_name: str):
        self.ddb_client = ddb_client
        self.table_name = table_name

    def put_item(self, item: dict) -> None:
        """
        Put item into client's DynamoDB table

        :param: item
        :returns: None
        """
        try:
            self.ddb_client.put_item(TableName=self.table_name, Item=item)
        except Exception as e:
            raise DdbTeamsWriteException(
                "Unable to write to DDB table: {err}".format(err=str(e))
            )
