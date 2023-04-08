from utils.constants import MAX_TEAMS, COMPOSITE_DELIMITER
from utils.base_logger import logger


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
            logger.error(
                "Unable to query team by ID from DDB table for {team_id}: {err}".format(
                    team_id=team_id, err=str(e)
                )
            )
            return {"error": "Internal error, please try again later"}

    def query_teams_by_format_and_date(self, format: str, date: str) -> dict:
        """
        Query teams by format and date via composite key
        Number of results constrained by MAX_LIMIT

        :param: format
        :param: date
        :returns: query response
        """
        composite_key = format + COMPOSITE_DELIMITER + date
        try:
            response = self.ddb_client.query(
                TableName=self.table_name,
                IndexName="formatSnapshotDateCompositeIndex",
                KeyConditionExpression="format_snapshot_date_composite = :format_snapshot_date_composite",
                ExpressionAttributeValues={
                    ":format_snapshot_date_composite": {"S": composite_key}
                },
                ScanIndexForward=False,
                Limit=MAX_TEAMS,
            )
            if "LastEvaluatedKey" in response.values():
                logger.warning(
                    "Request exceeded team query limit of ${limit}".format(
                        limit=MAX_TEAMS
                    )
                )
            return response
        except Exception as e:
            logger.error(
                "Unable to query team by '{format}' format from DDB table: {err}".format(
                    format=format, err=str(e)
                )
            )
            return {"error": "Internal error, please try again later"}
