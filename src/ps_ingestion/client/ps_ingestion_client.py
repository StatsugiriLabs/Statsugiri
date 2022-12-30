from data.ingest_data_info import IngestDataInfo
from modules.replay_handler import ReplayHandler
from modules.replay_parser import ReplayParser
from typing import List
from data.team_snapshot_info import TeamSnapshotInfo


class PsIngestionClient:
    def __init__(
        self,
        replay_handler: ReplayHandler,
        replay_parser: ReplayParser,
    ):
        self.replay_handler = replay_handler
        self.replay_parser = replay_parser

    """
    Facilitate ETL process for PS teams

    :param: ingest_data_info 
    :returns: teams_snapshot
    """

    def process(self, ingest_data_info: IngestDataInfo) -> List[TeamSnapshotInfo]:
        replays = self.replay_handler.extract_replays(
            ingest_data_info.num_users_to_pull
        )
        teams_snapshot = self.replay_parser.transform_to_teams_snapshot(
            replays, ingest_data_info
        )
        return teams_snapshot
