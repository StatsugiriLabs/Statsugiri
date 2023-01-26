import os

HTTP_BODY_KEY = "Body"
TEAMS_BUCKET_KEY_ARG = "bucket_key"
TEAMS_BUCKET_NAME_ARG = "bucket_name"
BUCKET_KEY_FIELD = "bucket_key"
BUCKET_NAME_FIELD = "bucket_name"

PAYLOAD_EVENT_ARG = "Payload"
SNAPSHOT_DATE_EVENT_ARG = "snapshot_date"
FORMAT_ID_EVENT_ARG = "format_id"
TEAM_LIST_EVENT_ARG = "team_list"
PKMN_TEAM_EVENT_ARG = "pkmn_team"
RATING_EVENT_ARG = "rating"
ID_EVENT_ARG = "id"

MAX_TWEET_LENGTH = 280
TWITTER_BASE_URL = "https://twitter.com"
REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/"
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_DISPLAY_NAME = os.environ.get("TWITTER_DISPLAY_NAME")
