from enum import IntEnum

from bs4 import BeautifulSoup
import requests


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
        response = requests.get(self.url)
        if response.status_code != Status.OK:
            print(f"Failed to fetch HTML. Status code: {response.status_code}")
            return None

        return response.text


class HtmlParser(HtmlFetcher):
    def __init__(self, url):
        super().__init__(url)
        self.html = self.fetch()
        self.soup = BeautifulSoup(self.html, "lxml") if self.html else None

    def set_soup(self, url):
        self.url = url
        self.html = self.fetch()
        self.soup = BeautifulSoup(self.html, "lxml") if self.html else None


if __name__ == '__main__':
    pass
