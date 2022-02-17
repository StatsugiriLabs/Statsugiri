""" Constants shared between modules """
from utils.env_configs import ENV

# PS! terms
# gen8vgc2021series11 is a legacy format primarily for tests
FORMATS = [
    "gen8vgc2021series11",
    "gen8vgc2022",
    "gen8doublesou",
    "gen8ou",
    "gen8nationaldexag",
    "gen8nationaldex",
    "gen8anythinggoes",
]
NUM_TEAMS = 50
MAX_USERS = 500
NUM_PARTNERS = 5
TEAM_SIZE = 6

# DB terms
DB_ENV_PREFIX = ENV + "_"
DB_CLUSTER_NAME = "babiri-dev-cluster"
POKEMON_TEAMS_SNAPSHOTS_COLLECTION = "pokemon_teams_snapshots"
POKEMON_USAGE_SNAPSHOTS_COLLECTION = "pokemon_usage_snapshots"
POKEMON_TEAMS_SNAPSHOTS_COLLECTION_NAME = (
    DB_ENV_PREFIX + POKEMON_TEAMS_SNAPSHOTS_COLLECTION
)
POKEMON_USAGE_SNAPSHOTS_COLLECTION_NAME = (
    DB_ENV_PREFIX + POKEMON_USAGE_SNAPSHOTS_COLLECTION
)
