from pathlib import Path


BASE_DIR = Path()
DATA_DIR = BASE_DIR.joinpath('data')

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

AUTHORS_DATA = DATA_DIR.joinpath('authors.json')
QUOTES_DATA = DATA_DIR.joinpath('quotes.json')

SCRAPE_URL = "http://quotes.toscrape.com/"


