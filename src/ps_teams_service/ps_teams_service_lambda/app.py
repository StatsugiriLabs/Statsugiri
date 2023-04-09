import boto3
import json
from lambda_typing.types import LambdaDict, LambdaContext
from clients.teams_ddb_client import TeamsDdbClient
from modules.ddb_teams_reader import DdbTeamsReader
from utils.base_logger import logger
from utils.constants import TABLE_NAME
from typing import List


GET_OPERATION = "GET"
GET_HEALTH_RESOURCE = "/health"
GET_TEAM_RESOURCE = "/team/{team_id}"
GET_TEAMS_RESOURCE = "/teams/{format}/{date}"
TEAM_ID_PARAM = "team_id"
DATE_PARAM = "date"
FORMAT_PARAM = "format"


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    logger.info(
        "Received {operation} request for {endpoint}".format(
            operation=event["httpMethod"], endpoint=event["path"]
        )
    )

    ddb_client = boto3.client("dynamodb")
    teams_ddb_client = TeamsDdbClient(ddb_client, TABLE_NAME)
    ddb_teams_reader = DdbTeamsReader(teams_ddb_client)
    res_body = {}

    if (
        event["httpMethod"] == GET_OPERATION
        and event["resource"] == GET_HEALTH_RESOURCE
    ):
        res_body = ddb_teams_reader.get_health_check()
    elif (
        event["httpMethod"] == GET_OPERATION and event["resource"] == GET_TEAM_RESOURCE
    ):
        team_id = event["pathParameters"][TEAM_ID_PARAM]
        res_body = ddb_teams_reader.get_team_by_id(team_id)
    elif (
        event["httpMethod"] == GET_OPERATION and event["resource"] == GET_TEAMS_RESOURCE
    ):
        query_string_params = event["queryStringParameters"]
        format = event["pathParameters"][FORMAT_PARAM]
        date = event["pathParameters"][DATE_PARAM]
        pkmn_to_filter = _transform_query_param_to_filter(query_string_params)

        res_body = ddb_teams_reader.get_teams_by_format_and_date(
            format, date, pkmn_to_filter
        )
    else:
        logger.warning("Route and HTTP method do not match...")
        res_body = {"Error": "Routing and HTTP method is invalid"}

    return _build_response(res_body)


def _build_response(res_body: dict):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(res_body),
    }


def _transform_query_param_to_filter(query_string_params: dict) -> List[str]:
    pkmn_to_filter = []
    pkmn_to_filter.extend(
        query_string_params["pkmn"] if "pkmn" not in query_string_params else []
    )
    pkmn_to_filter.extend(
        query_string_params["pkmn2"] if "pkmn2" not in query_string_params else []
    )
    pkmn_to_filter.extend(
        query_string_params["pkmn3"] if "pkmn3" not in query_string_params else []
    )
    pkmn_to_filter.extend(
        query_string_params["pkmn4"] if "pkmn4" not in query_string_params else []
    )
    pkmn_to_filter.extend(
        query_string_params["pkmn5"] if "pkmn5" not in query_string_params else []
    )
    pkmn_to_filter.extend(
        query_string_params["pkmn6"] if "pkmn6" not in query_string_params else []
    )
    return pkmn_to_filter
