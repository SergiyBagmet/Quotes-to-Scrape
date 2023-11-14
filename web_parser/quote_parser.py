import json
from itertools import chain

from base_parse import HtmlParser


class QuoteParser(HtmlParser):
    def __init__(self, url):
        super().__init__(url)
        self.base_url = url
        self.authors_ref = set()

    def parse_quotes(self) -> list[str]:
        quotes = self.soup.select(".quote span.text")
        return [quote.get_text() for quote in quotes]

    def parse_authors_name(self):
        authors_name = self.soup.select(".quote small.author")
        return [name.get_text() for name in authors_name]

    def parse_authors_url(self):
        authors_ref = self.soup.select(".quote span a")
        [self.authors_ref.add(ref["href"]) for ref in authors_ref]

    def parse_tags(self):
        tags_text = self.soup.select(".quote .tags")
        tags_quotes = [tags_quote.get_text(separator="\n", strip=True) for tags_quote in tags_text]
        return [tags.split('\n')[1:] for tags in tags_quotes]

    def get_next_page_url(self):
        next_page_url = self.soup.select(".next a")
        return self.base_url + next_page_url[0]["href"] if next_page_url else None

    def parse_page(self):
        self.parse_authors_url()

        return [{'tags': tags, 'author': author_name, 'quote': quote} for tags, author_name, quote in
                zip(self.parse_tags(), self.parse_authors_name(), self.parse_quotes())]

    def parse_pages(self, count: int | None = None):
        while True:
            yield self.parse_page()

            next_page_url = self.get_next_page_url()
            if count: count -= 1
            if (not next_page_url) or (count == 0):
                break

            self.set_soup(next_page_url)

    def quotes_to_json(self, file):
        data = list(chain(*self.parse_pages()))
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    q_parser = QuoteParser("http://quotes.toscrape.com/")
    q_parser.quotes_to_json('../scrape_data/quotes_data.json')

    for url in q_parser.authors_ref:
        print(url)
