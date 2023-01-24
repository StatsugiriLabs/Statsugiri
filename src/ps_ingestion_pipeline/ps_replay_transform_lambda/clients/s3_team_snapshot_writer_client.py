import pickle
from mypy_boto3_s3 import S3Client
from data.team_snapshot import TeamSnapshot
from utils.base_logger import logger
from utils.serdes_utils import to_dict
from utils.constants import KEY_DELIMITER
from utils.errors import ReplaysBucketUploadException, ReplaysBucketUploadException


class S3TeamSnapshotWriterClient:
    def __init__(self, s3_client: S3Client, teams_bucket_name: str):
        self.s3_client = s3_client
        self.teams_bucket_name = teams_bucket_name

    def write(self, team_snapshot: TeamSnapshot) -> str:
        """
        Write snapshot to S3 bucket

        :param: team_snapshot
        :returns: bucket key
        """
        team_snapshot_key = KEY_DELIMITER.join(
            [team_snapshot.format_id, team_snapshot.snapshot_date]
        )
        try:
            team_snapshot_pkl = self._to_pickle(team_snapshot)
            self.s3_client.put_object(
                Bucket=self.teams_bucket_name,
                Body=team_snapshot_pkl,
                Key=team_snapshot_key,
            )
            return team_snapshot_key
        except Exception as e:
            logger.error(
                "Cannot upload object to teams bucket:{err}".format(err=str(e))
            )
            raise ReplaysBucketUploadException()

    def _to_pickle(self, team_snapshot: TeamSnapshot) -> bytes:
        """
        Pickle (serialize) team snapshot

        :param: team_snapshot
        :returns: bytes (ie. pickled object)
        """
        # Pickle has difficulty deserializing to custom classes, hence dictionaries are used
        team_snapshot_dict = to_dict(team_snapshot)
        team_snapshot_pkl = pickle.dumps(team_snapshot_dict)
        return team_snapshot_pkl
