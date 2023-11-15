from enum import IntEnum

from bs4 import BeautifulSoup
import requests

from my_logger import MyLogger

logger_html = MyLogger('html', 10).get_logger()


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

    def fetch(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            logger_html.info(f"HTML fetched successfully from {self.url}")
            return response.text
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to fetch HTML from {self.url}. Error: {e}"
            logger_html.error(error_message)
            return None


class HtmlParser(HtmlFetcher):
    def __init__(self, url):
        super().__init__(url)
        self.html = self.fetch()
        self.soup = BeautifulSoup(self.html, "lxml") if self.html else None

    def set_page(self, url):
        self.url = url
        self.html = self.fetch()
        self.soup = BeautifulSoup(self.html, "lxml") if self.html else None


if __name__ == '__main__':
    pass
