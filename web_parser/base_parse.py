from enum import IntEnum

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests

from my_logger import logger


class Status(IntEnum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    SERVICE_UNAVAILABLE = 503
    BAD_GATEWAY = 502
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    BANDWIDTH_LIMIT_EXCEEDED = 509
    NOT_EXTENDED = 510


class HtmlFetcher:
    def __init__(self, url):
        self.url = url
        self.user_agent = UserAgent()
        self.session = requests.Session()
        self.login_status: bool | None = None

    def login(self, login_ref, login_data):
        login_url = self.url + login_ref
        headers = {'User-Agent': self.user_agent.random}
        response = self.session.post(login_url, data=login_data, headers=headers, timeout=10)
        if response.status_code == Status.OK:
            self.login_status = True
            logger.info(f"Login successful from {login_url}")
            return response.text
        else:
            self.login_status = False
            logger.warning(f"Login unsuccessful from {login_url}. Check credentials.")
            return None

    def fetch(self):
        try:
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()
            logger.info(f"HTML fetched successfully from {self.url}")
            return response.text
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to fetch HTML from {self.url}. Error: {e}"
            logger.error(error_message)
            return None


class HtmlParser(HtmlFetcher):
    def __init__(self, url, login_ref, login_data):
        super().__init__(url)
        self.login_ref = login_ref
        self.login_data = login_data
        self.html = self.login(login_ref, login_data)
        self.soup = BeautifulSoup(self.html, "lxml") if self.html else None

    def set_page(self, url):
        self.url = url
        self.html = self.fetch()
        self.soup = BeautifulSoup(self.html, "lxml") if self.html else None


if __name__ == '__main__':
    pass
