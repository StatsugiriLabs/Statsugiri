import os

CURR_VGC_FORMAT = "gen9vgc2023regulatione"
CURR_VGC_FORMAT_BO3 = "gen9vgc2023regulationebo3"
VALID_FORMATS = [
    CURR_VGC_FORMAT,
    CURR_VGC_FORMAT_BO3,
    "gen9ou",
]

EVENT_FORMAT_KEY = "format"
SNAPSHOT_DATE_KEY = "snapshot_date"
BUCKET_KEY_FIELD = "bucket_key"
BUCKET_NAME_FIELD = "bucket_name"
NUM_USERS_TO_PULL = os.environ.get("NUM_USERS_TO_PULL", "100")
MAX_USERS = 500
REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/"
REQUEST_TIMEOUT = 5  # [seconds]
REPLAYS_BUCKET_NAME = os.environ.get("REPLAYS_BUCKET_NAME", "")
KEY_DELIMITER = "#"
DAY_IN_SECONDS = 60 * 60 * 24
