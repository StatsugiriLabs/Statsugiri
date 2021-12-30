"""Unit tests for `LogHandler` class"""
import os
import pytest
from log_handler import LogHandler

@pytest.fixture(name="log_handler_under_test")
def fixture_log_handler():
    """Initialize log handler for tests"""
    return LogHandler()

@pytest.fixture(name="sample_log_json")
def fixture_sample_log_json():
    """Read sample log JSON response for mocking GET request"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return open(
        os.path.join(__location__, "assets/sample_log.json.txt"),
        encoding="utf-8",
    ).read()