""" Constants shared between modules """
import os
import json

CURR_DIR = os.path.dirname(__file__)

# Read from JSON configs
with open(os.path.join(CURR_DIR, "../shared/formats.json")) as json_file:
    formats_json = json.load(json_file)

# PS! terms
FORMATS = formats_json["formats"]
NUM_TEAMS = 10
MAX_USERS = 500
NUM_PARTNERS = 5
TEAM_SIZE = 6

# DB terms
DB_ENV_PREFIX = "PROD_" if os.getenv("ENV", "") == "PROD" else "DEV_"
# TODO: Convert to env var
DB_CLUSTER_NAME = "babiri-dev-cluster"
POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME = DB_ENV_PREFIX + "pokemon_teams_snapshots"
POKEMON_USAGE_SNAPSHOTS_COLLECTION_NAME = DB_ENV_PREFIX + "pokemon_usage_snapshots"
