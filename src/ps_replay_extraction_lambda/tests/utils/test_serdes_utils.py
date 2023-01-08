from utils.serdes_utils import to_dict
from data.replay_snapshot import ReplaySnapshot
from data.replay_info import ReplayInfo


def test_to_dict_happy_path():
    snapshot = ReplaySnapshot(
        "2022-01-01",
        "test_format",
        [
            ReplayInfo(1, "user1", 1001, "test_format", "log1", "2022-01-01"),
            ReplayInfo(2, "user2", 1002, "test_format", "log2", "2022-01-02"),
        ],
    )
    snapshot_json = to_dict(snapshot)
    expected_json = {
        "snapshot_date": "2022-01-01",
        "format_id": "test_format",
        "replay_list": [
            {
                "id": 1,
                "username": "user1",
                "rating": 1001,
                "format": "test_format",
                "log": "log1",
                "upload_date": "2022-01-01",
            },
            {
                "id": 2,
                "username": "user2",
                "rating": 1002,
                "format": "test_format",
                "log": "log2",
                "upload_date": "2022-01-02",
            },
        ],
    }
    assert snapshot_json == expected_json
