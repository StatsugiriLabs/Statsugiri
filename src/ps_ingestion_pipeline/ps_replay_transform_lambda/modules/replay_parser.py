import re
from typing import List
from utils.constants import TEAM_SIZE
from utils.base_logger import logger
from utils.errors import NoUserProvidedException

ARTIFACTS = [
    "-*",
    "-Four",  # Maushold-Four functionally identical to Maushold default (ie. Maushold Family-of-Three)
    "-Curly",  # Record Tatsugiri ignoring form
    "-Stretchy",
    "-Droopy",
]


class ReplayParser:
    def parse_team(self, username: str, replay_log: str) -> List[str]:
        """
        Parse replay log for a user's team

        :param: username
        :param: replay_log
        :returns: team of the user
        """
        if not username:
            logger.error("Invalid username, cannot proceed")
            raise NoUserProvidedException("Invalid username provided for parsing team")

        replay_log = self._sanitize_replay(replay_log)

        # Identify whether user is `p1` or `p2`
        # Ex. |player|p1|<PLAYER>|265|1546
        alphanumeric_username = self._generate_alphanumeric_username_regex(username)
        player_num = re.findall(
            f"\\|player\\|(\\w+)\\|{alphanumeric_username}\\|",
            replay_log,
            re.IGNORECASE,
        )
        if not player_num:
            logger.warning(
                "Could not properly locate player ID for {username} in log".format(
                    username=username
                )
            )
            return self._fill_team()

        # Identify the player's team
        # Ex. |poke|p1|<PKMN>, L50, F| or |poke|p1|<PKMN>|
        # '([\w':-]+)' regex for hyphens (eg. Rotom-Heat) and colons (eg. Type:Null)
        pkmn_team = re.findall(
            f"\\|poke\\|{player_num[0]}\\|([\\w\\s':-]+)", replay_log
        )
        if not pkmn_team:
            logger.warning("Cannot parse team in log, team not found")
            return self._fill_team()

        return self._fill_team(pkmn_team)

    def _sanitize_replay(self, replay_log: str) -> str:
        """
        Sanitize replay log for artifacts (eg. ambiguous form notation)

        :param: replay_log
        :returns: sanitized log
        """
        for artifact in ARTIFACTS:
            replay_log = replay_log.replace(artifact, "")
        return replay_log

    def _fill_team(self, pkmn_team: List[str] = None) -> List[str]:
        """
        Fill team to TEAM_SIZE with placeholder values (ie. pkmn0)

        :param: pkmn_team
        :returns: pkmn_team filled to TEAM_SIZE
        """
        pkmn_team = [] if not pkmn_team else pkmn_team
        return pkmn_team + [
            "pkmn" + str(slot) for slot in range(len(pkmn_team), TEAM_SIZE)
        ]

    def _generate_alphanumeric_username_regex(self, username: str) -> str:
        """
        Generate username regex ignoring non-alphanumeric characters (eg. whitespace, footstops, etc)
        https://stackoverflow.com/questions/6053541/regex-every-non-alphanumeric-character-except-white-space-or-colon

        :param: username
        :returns: regex ignoring special chars
        """
        # PS does not ignore underscores, so an explicit check is required
        alphanumeric_username = "".join(ch for ch in username if ch.isalnum())
        return (
            "[^A-Za-z0-9]*"
            + "[^A-Za-z0-9]*".join(alphanumeric_username)
            + "[^A-Za-z0-9]*"
        )
