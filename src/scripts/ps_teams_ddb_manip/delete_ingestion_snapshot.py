import boto3
import logging
import datetime
import time

TABLE_NAME_BASE = "PsIngestionTeamsTable"
ENV_LIST = ["Beta", "Prod"]
INDEX_NAME = "formatSnapshotDateCompositeIndex"
MAX_TEAMS = 100

# Initialize logger
logger = logging.getLogger()
logging.basicConfig(format="%(message)s")
logger.setLevel(logging.INFO)


def main():
    ddb_client = boto3.client("dynamodb")
    logger.info(
        "WARNING: This script is for deleting ingestion data and may have a large blast radius. Proceed with caution."
    )

    # Gather parameters
    env = input(
        "🔵 Please provide the environment (case-sensitive). Environments: {env_list}.\n".format(
            env_list=ENV_LIST
        )
    ).strip()
    while env not in ENV_LIST:
        env = input(
            "🔵 Try again. Note case-sensitivity. Environments: {env_list}.\n".format(
                env_list=ENV_LIST
            )
        ).strip()
    table_name = TABLE_NAME_BASE + "-" + env

    date = input("🔵 Please provide the date. Format must be 'YYYY-MM-DD'.\n").strip()
    while not validate_date(date):
        date = input("🔵 Try again. Format must be 'YYYY-MM-DD.\n").strip()

    format = input("🔵 Please provide the format.\n").strip()
    comp_key = format + "#" + date

    # Query items to be deleted
    logger.info(
        "Initializing deletion for '{format}' on '{date}' under table '{table}'".format(
            format=format, date=date, table=table_name
        )
    )

    response = ddb_client.query(
        TableName=table_name,
        IndexName=INDEX_NAME,
        KeyConditionExpression="format_snapshot_date_composite = :format_snapshot_date_composite",
        ExpressionAttributeValues={":format_snapshot_date_composite": {"S": comp_key}},
        Limit=MAX_TEAMS,
    )

    # Confirm with user to proceed
    num_items = len(response["Items"])
    confirmation = input(
        "🔵 {num_items} found in '{table}'. Press 'Y' to proceed with deletion.\n".format(
            num_items=num_items, table=table_name
        )
    ).strip()
    if confirmation != "Y":
        logger.info("🔵 No confirmation provided. Deletion script is aborting.")
        exit()

    start_time = time.time()
    # Delete processing
    for item in response["Items"]:
        team_id = item["team_id"]["S"]
        response = ddb_client.delete_item(
            TableName=table_name,
            Key={
                "team_id": {"S": team_id},
                "format_snapshot_date_composite": {"S": comp_key},
            },
        )

    logger.info(
        "🔵 {num_items} items have been deleted in {time} seconds. Deletion script is complete.".format(
            num_items=num_items, time=str(time.time() - start_time)
        )
    )


# Validate provided date string adheres to 'YYYY-MM-DD' format
def validate_date(date_str: str) -> bool:
    try:
        datetime.date.fromisoformat(date_str)
        return True
    except ValueError:
        logger.warning("Incorrect format, should be YYYY-MM-DD")
        return False


if __name__ == "__main__":
    main()
