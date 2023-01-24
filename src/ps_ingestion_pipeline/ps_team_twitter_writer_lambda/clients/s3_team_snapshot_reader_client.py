import pickle
from mypy_boto3_s3 import S3Client
from utils.base_logger import logger
from utils.errors import ReplaysBucketDownloadException
from utils.constants import HTTP_BODY_KEY


class S3TeamSnapshotReaderClient:
    def __init__(self, s3_client: S3Client, teams_bucket_name: str):
        self.s3_client = s3_client
        self.teams_bucket_name = teams_bucket_name

    def read(self, key: str) -> dict:
        """
        Read team snapshot from S3 bucket

        :param: key
        :returns: team snapshot dictionary
        """
        try:
            teams_bucket_res = self.s3_client.get_object(
                Bucket=self.teams_bucket_name, Key=key
            )
            team_snapshot = pickle.loads(teams_bucket_res[HTTP_BODY_KEY].read())
            return team_snapshot
        except Exception as e:
            logger.error(
                "Cannot download object from teams bucket:{err}".format(err=str(e))
            )
            raise ReplaysBucketDownloadException()
