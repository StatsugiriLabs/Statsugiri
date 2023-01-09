from lambda_typing.types import LambdaDict
from modules.replay_parser import ReplayParser
from data.team_snapshot import TeamSnapshot
from data.team_info import TeamInfo
from utils.constants import (
    SNAPSHOT_DATE_EVENT_ARG,
    FORMAT_ID_EVENT_ARG,
    REPLAY_LIST_EVENT_ARG,
    REPLAY_ID_EVENT_ARG,
    REPLAY_USERNAME_EVENT_ARG,
    REPLAY_RATING_EVENT_ARG,
    REPLAY_LOG_EVENT_ARG,
    REPLAY_UPLOAD_DATE_EVENT_ARG,
)


class PsReplayTransformClient:
    def __init__(self, replay_parser: ReplayParser):
        self.replay_parser = replay_parser

    def transform(self, replay_snapshot_event: LambdaDict) -> TeamSnapshot:
        """
        Transform incoming replay snapshot event to team snapshot
        :param: replay_snapshot_event
        :returns: TeamSnapshot
        """
        team_list = []
        for replay in replay_snapshot_event[REPLAY_LIST_EVENT_ARG]:
            pkmn_team = self.replay_parser.parse_team(
                replay[REPLAY_USERNAME_EVENT_ARG], replay[REPLAY_LOG_EVENT_ARG]
            )
            team = TeamInfo(
                replay[REPLAY_ID_EVENT_ARG],
                pkmn_team,
                replay[REPLAY_RATING_EVENT_ARG],
                replay[REPLAY_UPLOAD_DATE_EVENT_ARG],
            )
            team_list.append(team)

        team_snapshot = TeamSnapshot(
            replay_snapshot_event[SNAPSHOT_DATE_EVENT_ARG],
            replay_snapshot_event[FORMAT_ID_EVENT_ARG],
            team_list,
        )
        return team_snapshot
