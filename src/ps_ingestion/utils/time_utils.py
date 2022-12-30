"""Time utility functions"""
from datetime import datetime

"""
Convert unix timestamp to 'yyyy-mm-dd' format string

:param: timestamp 
:returns: str representing 'yyyy-mm-dd' str
"""


def convert_unix_timestamp_to_str(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
