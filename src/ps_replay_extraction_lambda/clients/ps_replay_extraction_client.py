from modules.replay_extractor import ReplayExtractor
from data.replay_snapshot import ReplaySnapshot


class PsReplayExtractionClient:
    def __init__(
        self,
        replay_extractor: ReplayExtractor,
    ):
        self.replay_extractor = replay_extractor

    def process(self) -> ReplaySnapshot:
        """
        Facilitate replay extraction for top ladder users

        :param: ingest_data_info
        :returns: replay_snapshot
        """
        replay_snapshot = self.replay_extractor.get_replay_snapshot()
        return replay_snapshot
