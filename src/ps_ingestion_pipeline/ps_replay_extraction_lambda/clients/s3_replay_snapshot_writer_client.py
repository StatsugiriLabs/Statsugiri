import pickle
from mypy_boto3_s3 import S3Client
from data.replay_snapshot import ReplaySnapshot
from utils.base_logger import logger
from utils.serdes_utils import to_dict
from utils.constants import KEY_DELIMITER
from utils.errors import ReplaysBucketUploadException


class S3ReplaySnapshotWriterClient:
    def __init__(self, s3_client: S3Client, replays_bucket_name: str):
        self.s3_client = s3_client
        self.replays_bucket_name = replays_bucket_name

    def write(self, replay_snapshot: ReplaySnapshot) -> str:
        """
        Write snapshot to S3 bucket

        :param: replay_snapshot
        :returns: bucket key
        """
        replay_snapshot_key = KEY_DELIMITER.join(
            [replay_snapshot.format_id, replay_snapshot.snapshot_date]
        )
        try:
            replay_snapshot_pkl = self._to_pickle(replay_snapshot)
            self.s3_client.put_object(
                Bucket=self.replays_bucket_name,
                Body=replay_snapshot_pkl,
                Key=replay_snapshot_key,
            )
            return replay_snapshot_key
        except Exception as e:
            logger.error(
                "Cannot upload object to replays bucket:{err}".format(err=str(e))
            )
            raise ReplaysBucketUploadException()

    def _to_pickle(self, replay_snapshot: ReplaySnapshot) -> bytes:
        """
        Pickle (serialize) replay snapshot

        :param: replay_snapshot
        :returns: bytes (ie. pickled object)
        """
        # Pickle has difficulty deserializing to custom classes, hence dictionaries are used
        replay_snapshot_dict = to_dict(replay_snapshot)
        replay_snapshot_pkl = pickle.dumps(replay_snapshot_dict)
        return replay_snapshot_pkl
