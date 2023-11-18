from seeds import run_seeder
from web_parser.quote_parser import QuoteParser, data_to_json
from search_quotes import search
from src.crud import MongoCRUD
from name_space import AUTHORS_DATA, QUOTES_DATA, SCRAPE_URL, LOGIN_REF, LOGIN_DATA


def main():
    parser = QuoteParser(SCRAPE_URL, LOGIN_REF, LOGIN_DATA)
    quotes, authors = parser.parse_pages()
    data_to_json(QUOTES_DATA, quotes)
    data_to_json(AUTHORS_DATA, authors)

    crud = MongoCRUD()

    run_seeder(crud, AUTHORS_DATA, QUOTES_DATA)

    search(crud)


if __name__ == '__main__':
    main()
