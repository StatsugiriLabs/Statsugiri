""" Log Handler is responsible for parsing metadata and replay logs into structured information """
import re
from replay_metadata import ParsedReplay


class LogHandler:
    def __init__(self):
        self.parsed_replay = ParsedReplay()
        # TODO: Transformers will make use of ParsedReplay state from `data_extractor`` layer

    def parse_users(self) -> None:
        """ Parse for players and store in `parsed_replay` """
        # TODO: Check sanitized_log is populated
        # TODO: Check users parsed are different
        sanitized_log = self.parsed_replay.get_sanitized_log()
        # TODO: Handle cases where no user found
        p1_user = re.findall("\\|player\\|p1\\|(.*?)\\|", sanitized_log)[0]
        p2_user = re.findall("\\|player\\|p2\\|(.*?)\\|", sanitized_log)[0]
        self.parsed_replay.set_p1_user(p1_user)
        self.parsed_replay.set_p2_user(p2_user)

    def parse_teams(self) -> None:
        """ Parse for teams and store in `parsed_replay` """
        sanitized_log = self.parsed_replay.get_sanitized_log()
        p1_team = re.findall("\\|poke\\|p1\\|(.*?),", sanitized_log)
        p2_team = re.findall("\\|poke\\|p2\\|(.*?),", sanitized_log)
        # TODO: Check p1 and p2 are populated
        p1_user = self.parsed_replay.get_p1_user()
        p2_user = self.parsed_replay.get_p2_user()
        self.parsed_replay.set_teams(p1_user, p2_user, p1_team, p2_team)
        breakpoint()

    def feed(self, replay_data: dict):
        """ Clean replay data and populate metadata from log """
        # Sanitize alternate form names
        sanitized_log = replay_data["log"].replace("-*", "")
        self.parsed_replay.set_sanitized_log(sanitized_log)
        # TODO: Check this logic
        self.parsed_replay.set_replay_metadata(replay_data["uploadtime"], replay_data["id"], replay_data["formatid"])

    def parse(self):
        """ Transform and store cleaned log into `ParsedReplay` data """
        """ Return True if replay data successfully parsed """
        # TODO: Verify `feed` has been called
        self.parse_users()
        self.parse_teams()
