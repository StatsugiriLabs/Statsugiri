from utils.time_utils import convert_unix_timestamp_to_str


def test_convert_unix_timestamp_to_str_happy_path():
    date_str = convert_unix_timestamp_to_str(1606662312)
    assert date_str == "2020-11-29"
