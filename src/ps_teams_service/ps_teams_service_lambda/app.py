import boto3
import json
import time
from lambda_typing.types import LambdaDict, LambdaContext
from clients.teams_ddb_client import TeamsDdbClient
from modules.ddb_teams_reader import DdbTeamsReader
from utils.time_utils import convert_unix_timestamp_to_str
from utils.base_logger import logger
from utils.constants import TABLE_NAME
from typing import List


GET_OPERATION = "GET"
GET_HEALTH_RESOURCE = "/health"
GET_TEAM_RESOURCE = "/team/{team_id}"
GET_TEAMS_RESOURCE = "/teams/{format}/{date}"
GET_TEAM_TODAY_RESOURCE = "/teams/{format}/today"
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
    elif (
        event["httpMethod"] == GET_OPERATION
        and event["resource"] == GET_TEAM_TODAY_RESOURCE
    ):
        query_string_params = event["queryStringParameters"]
        format = event["pathParameters"][FORMAT_PARAM]
        date = convert_unix_timestamp_to_str(int(time.time()))
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
    if not query_string_params:
        return []

    pkmn_to_filter = []
    if "pkmn" in query_string_params:
        pkmn_to_filter.append(query_string_params["pkmn"].lower())
    if "pkmn2" in query_string_params:
        pkmn_to_filter.append(query_string_params["pkmn2"].lower())
    if "pkmn3" in query_string_params:
        pkmn_to_filter.append(query_string_params["pkmn3"].lower())
    if "pkmn4" in query_string_params:
        pkmn_to_filter.append(query_string_params["pkmn4"].lower())
    if "pkmn5" in query_string_params:
        pkmn_to_filter.append(query_string_params["pkmn5"].lower())
    if "pkmn6" in query_string_params:
        pkmn_to_filter.append(query_string_params["pkmn6"].lower())

    return pkmn_to_filter
