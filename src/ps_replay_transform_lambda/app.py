from lambda_typing.types import LambdaDict, LambdaContext
from clients.ps_replay_transform_client import PsReplayTransformClient
from modules.replay_parser import ReplayParser
from utils.constants import FORMAT_ID_EVENT_ARG, PAYLOAD_EVENT_ARG
from utils.base_logger import logger
from utils.serdes_utils import to_dict


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: team snapshot JSON
    """
    replay_snapshot_payload = event[PAYLOAD_EVENT_ARG]
    replay_snapshot_format = replay_snapshot_payload[FORMAT_ID_EVENT_ARG]
    logger.info("Incoming request for '{format}".format(format=replay_snapshot_format))

    ps_replay_transform_client = PsReplayTransformClient(ReplayParser())

    team_snapshot = ps_replay_transform_client.transform(replay_snapshot_payload)
    return to_dict(team_snapshot)
