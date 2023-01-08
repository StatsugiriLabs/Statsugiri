import json
import time
from lambda_typing.types import LambdaDict, LambdaContext


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: HTTP response
    """
    return "test works"
