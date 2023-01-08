# -*- coding: utf-8 -*-

from typing import Dict, Any

__all__ = ['LambdaDict',
           'LambdaCognitoIdentity',
           'LambdaClientContextMobileClient',
           'LambdaClientContext',
           'LambdaContext']

LambdaDict = Dict[str, Any]


class LambdaCognitoIdentity:
    cognito_identity_id: str
    cognito_identity_pool_id: str


class LambdaClientContextMobileClient:
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str


class LambdaClientContext:
    client: LambdaClientContextMobileClient
    custom: LambdaDict
    env: LambdaDict


# https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
# https://gist.github.com/alexcasalboni/a545b68ee164b165a74a20a5fee9d13
class LambdaContext:
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: LambdaCognitoIdentity
    client_context: LambdaClientContext

    @staticmethod
    def get_remaining_time_in_millis() -> int:
        return 0
