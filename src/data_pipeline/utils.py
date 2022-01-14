"""Utility functions for Drilbur"""
from datetime import datetime


def convert_unix_timestamp_to_str(timestamp: int) -> str:
    """Convert unix timestamp to 'yyyy-mm-dd' format string"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
