import requests
from bs4 import BeautifulSoup
from utils.constants import REQUEST_TIMEOUT
from utils.base_logger import logger

"""
Wrapper for converting HTTP requests to BeautifulSoup representation

:param: request_url 
:returns: BeautifulSoup
"""


def get_soup_from_url(request_url: str) -> BeautifulSoup:
    logger.info("Making request to: {url}".format(url=request_url))
    try:
        ladder_res = requests.get(request_url, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(ladder_res.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        raise e
