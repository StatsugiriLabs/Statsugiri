from lambda_typing.types import LambdaDict
from modules.twitter_team_writer import TwitterTeamWriter


class PsTeamTwitterWriterClient:
    def __init__(self, twitter_team_writer: TwitterTeamWriter):
        self.twitter_team_writer = twitter_team_writer

    def write(self, team_snapshot_dict: dict) -> bool:
        """
        Transform incoming replay snapshot dict to team snapshot
        :param: replay_snapshot_dict
        :returns: success
        """
        success = self.twitter_team_writer.write(team_snapshot_dict)
        return success
