from utils.base_logger import logger
import re
from typing import List
from data.replay_info import ReplayInfo
from data.team_snapshot_info import TeamSnapshotInfo
from utils.time_utils import convert_unix_timestamp_to_str
from utils.constants import TEAM_SIZE

MULTIPLE_FORM_NOTATION = "-*"


class ReplayParser:
    """
    Transforms list of replays to a dated snapshot

    :param: replay_info_list
    :param: snapshot_timestamp Timestamp from when snapshot was taken
    :returns: list of snapshots for the snapshot date
    """

    def transform_to_teams_snapshot(
        self, replay_info_list: List[ReplayInfo], snapshot_date: str
    ) -> List[TeamSnapshotInfo]:
        teams_snapshot_list = []
        for replay_info in replay_info_list:
            team = self._parse_team(replay_info.username, replay_info.log)

            replay_upload_date = convert_unix_timestamp_to_str(replay_info.upload_time)
            teams_snapshot = TeamSnapshotInfo(
                replay_info.id,
                team,
                snapshot_date,
                replay_info.rating,
                replay_upload_date,
                replay_info.format,
            )
            teams_snapshot_list.append(teams_snapshot)
            logger.info(
                "{id}: {team}".format(
                    id=teams_snapshot.id, team=teams_snapshot.pkmn_team
                )
            )

        return teams_snapshot_list

    """
    Parse replay log for a user's team

    :param: username
    :param: replay_log
    :returns: team of the user
    """

    def _parse_team(self, username: str, replay_log: str) -> List[str]:
        # Sanitize log for Pokémon with multiple forms (ie. remove names appended with '-*')
        replay_log = replay_log.replace(MULTIPLE_FORM_NOTATION, "")

        if not username:
            logger.warning("Invalid username, cannot proceed")

        # Identify whether user is `p1` or `p2`
        # Ex. |player|p1|<PLAYER>|265|1546
        alphanumeric_username = self._generate_alphanumeric_username_regex(username)
        player_num = re.findall(
            f"\\|player\\|(\w+)\\|{alphanumeric_username}\\|", replay_log, re.IGNORECASE
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
        pkmn_team = re.findall(f"\\|poke\\|{player_num[0]}\\|([\w':-]+)", replay_log)
        if not pkmn_team:
            logger.warning("Cannot parse team in log, team not found")
            return self._fill_team()

        return self._fill_team(pkmn_team)

    """
    Fill team to TEAM_SIZE with placeholder values (ie. pkmn0)

    :param: pkmn_team
    :returns: pkmn_team filled to TEAM_SIZE
    """

    def _fill_team(self, pkmn_team: List[str] = None) -> List[str]:
        pkmn_team = [] if not pkmn_team else pkmn_team
        return pkmn_team + [
            "pkmn" + str(slot) for slot in range(len(pkmn_team), TEAM_SIZE)
        ]

    """
    Generate username regex ignoring non-alphanumeric characters (eg. whitespace, footstops, etc)
    https://stackoverflow.com/questions/4590298/
    how-to-ignore-whitespace-in-a-regular-expression-subject-string

    :param: username
    :returns: regex ignoring spaces (eg. 'b _ob' -> '\W*b\s*\W*_\s*\W*b\W*')
    """

    def _generate_alphanumeric_username_regex(self, username: str) -> str:
        # PS does not ignore underscores, so an explicit check is required
        alphanumeric_username = "".join(
            ch for ch in username if ch.isalnum() or ch == "_"
        )
        # \s* - Capture potential spaces
        # \W* - Capture non-alphanumeric characters
        return "\W*" + "\s*\W*".join(alphanumeric_username) + "\W*"
