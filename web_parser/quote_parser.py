import json
from itertools import chain

from bs4 import Tag

from base_parse import HtmlParser


class QuoteParser(HtmlParser):
    def __init__(self, url):
        super().__init__(url)
        self.base_url = url
        self.authors_ref = set()

        self.quotes_data = []
        self.authors_data = []

    def parse_quote_card(self, card: Tag):
        quote = card.find(class_='text').get_text()
        author_name = card.find(class_='author').get_text()
        tags = card.find(class_='tags').get_text(separator="\n", strip=True).split('\n')[1:]

        self.quotes_data.append(
            {
                "tags": tags,
                "author": author_name,
                "quote": quote,
            }
        )

        author_ref = card.find(class_='author').find_next("a")["href"]
        self.parse_author_ref(author_ref)

    def parse_author_ref(self, author_ref):
        if author_ref not in self.authors_ref:
            self.authors_ref.add(author_ref)
            self.set_page(self.base_url + author_ref)

            fullname = self.soup.find(class_="author-title").get_text()
            born_date = self.soup.find(class_="author-born-date").get_text()
            born_location = self.soup.find(class_="author-born-location").get_text()
            description = self.soup.find(class_="author-description").get_text(strip=True)
            self.authors_data.append(
                {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description,
                }
            )

    def get_next_page_url(self):
        next_page_url = self.soup.select(".next a")
        return self.base_url + next_page_url[0]["href"] if next_page_url else None

    def parse_page(self):
        cards = self.soup.find_all(class_='quote')
        for card in cards:
            self.parse_quote_card(card)

    def parse_pages(self, count: int | None = None):
        while True:
            next_page_url = self.get_next_page_url()
            self.parse_page()
            if count: count -= 1
            if (not next_page_url) or (count == 0):
                break

            self.set_page(next_page_url)

        return self.quotes_data, self.authors_data

    @staticmethod
    def data_to_json(filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    q_parser = QuoteParser("http://quotes.toscrape.com/")
    q_parser.parse_pages()
    q_parser.data_to_json("../scrape_data/quotes_data.json", q_parser.quotes_data)
    q_parser.data_to_json("../scrape_data/authors_data.json", q_parser.authors_data)
