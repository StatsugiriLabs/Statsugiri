""" Constants shared between modules """
import os

# PS! terms
FORMATS = ["gen8vgc2021series11", "gen8ou"]
NUM_TEAMS = 10
MAX_USERS = 500
NUM_PARTNERS = 5
TEAM_SIZE = 6

# DB terms
DB_ENV_PREFIX = "PROD_" if os.getenv("ENV", "") == "PROD" else "DEV_"
DB_CLUSTER_NAME = "babiri-dev-cluster"
POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME = DB_ENV_PREFIX + "pokemon_teams_snapshots"
POKEMON_USAGE_SNAPSHOTS_COLLECTION_NAME = DB_ENV_PREFIX + "pokemon_usage_snapshots"
