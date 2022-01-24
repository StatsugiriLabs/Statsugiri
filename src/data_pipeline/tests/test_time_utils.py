""" Unit tests for utility functions"""
from utils.time_utils import convert_unix_timestamp_to_str


def test_convert_unix_timestamp_to_str_happy_path():
    """Test converting from Unix timestamp to string format 'yyyy-mm-dd'"""
    date_str = convert_unix_timestamp_to_str(1606662312)
    assert date_str == "2020-11-29"
