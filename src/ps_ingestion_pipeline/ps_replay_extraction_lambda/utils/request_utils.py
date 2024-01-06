import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from utils.base_logger import logger
from utils.constants import REQUEST_TIMEOUT


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """
    Wrapper for creating HTTP session with retry
    https://www.peterbe.com/plog/best-practice-with-retries-with-requests

    :param: retries
    :param: backoff_factor the factor to delay for next retry
    :param: status_forcelist
    :param: session
    :returns: Session with retry
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_response_from_url(request_url: str) -> requests.Response:
    """
    Wrapper for converting HTTP requests to HTTP response

    :param: request_url
    :returns: Response
    """
    try:
        response = requests_retry_session().get(request_url, timeout=REQUEST_TIMEOUT)
        return response
    except requests.exceptions.RequestException as e:
        raise e


def get_soup_from_url(request_url: str) -> BeautifulSoup:
    """
    Wrapper for converting HTTP requests to BeautifulSoup representation

    :param: request_url
    :returns: BeautifulSoup
    """
    response = get_response_from_url(request_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
