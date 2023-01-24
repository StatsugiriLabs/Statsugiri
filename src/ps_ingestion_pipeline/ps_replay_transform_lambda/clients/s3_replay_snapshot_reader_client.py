import pickle
from mypy_boto3_s3 import S3Client
from utils.base_logger import logger
from utils.errors import ReplaysBucketDownloadException
from utils.constants import HTTP_BODY_KEY


class S3ReplaySnapshotReaderClient:
    def __init__(self, s3_client: S3Client, replays_bucket_name: str):
        self.s3_client = s3_client
        self.replays_bucket_name = replays_bucket_name

    def read(self, key: str) -> dict:
        """
        Read replay snapshot from S3 bucket

        :param: key
        :returns: replay snapshot dictionary
        """
        try:
            replays_bucket_res = self.s3_client.get_object(
                Bucket=self.replays_bucket_name, Key=key
            )
            replay_snapshot = pickle.loads(replays_bucket_res[HTTP_BODY_KEY].read())
            return replay_snapshot
        except Exception as e:
            logger.error(
                "Cannot download object from replays bucket:{err}".format(err=str(e))
            )
            raise ReplaysBucketDownloadException()
