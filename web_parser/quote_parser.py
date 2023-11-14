from abc_scrape import HtmlParser


class QuoteParser(HtmlParser):
    def __init__(self, url):
        super().__init__(url)
        self.base_url = url

    def parse_quotes(self) -> list[str]:
        quotes = self.soup.select(".quote span.text")
        return [quote.get_text() for quote in quotes]

    def parse_authors_name(self):
        authors_name = self.soup.select(".quote small.author")
        return [name.get_text() for name in authors_name]

    def parse_tags(self):
        tags_text = self.soup.select(".quote .tags")
        tags_quotes = [tags_quote.get_text(separator="\n", strip=True) for tags_quote in tags_text]
        return [tags.split('\n')[1:] for tags in tags_quotes]

    def get_next_page_url(self):
        next_page_url = self.soup.select(".next a")
        return self.base_url + next_page_url[0]["href"] if next_page_url else None

    def parse_page(self):
        self.parse_quotes()
        self.parse_authors_name()
        self.parse_tags()
        # some_save_to_file
        self.get_next_page_url()

    def parse_pages(self, count: int | None = None):
        pass


if __name__ == '__main__':
    s = QuoteParser("http://quotes.toscrape.com/")
    s.parse_page()
