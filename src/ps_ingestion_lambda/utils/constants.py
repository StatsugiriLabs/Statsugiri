import os

CURR_VGC_FORMAT = ("gen9vgc2023series1",)
VALID_FORMATS = [
    CURR_VGC_FORMAT,
    "gen9ou",
]

EVENT_FORMAT_KEY = "format"
NUM_USERS_TO_PULL = 3
MAX_USERS = 500
TEAM_SIZE = 6
REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/"
REPLAY_SEARCH_BASE_URL = "https://replay.pokemonshowdown.com/search/?output=html&user="
REQUEST_TIMEOUT = 120  # [seconds]

TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
# Prod: OrderUpTeamsBot
# Dev: TestOrderUpBot
TWITTER_DISPLAY_NAME = os.environ.get("TWITTER_DISPLAY_NAME")
