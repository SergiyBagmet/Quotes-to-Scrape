from redis_lru import RedisLRU

from src.config import mongo_uri, db_name, client
from src.models import Quote, Author
from src.crud import MongoCRUD
from src.db import MongoDBConnection

mongo_connection = MongoDBConnection(db_uri=mongo_uri)


class QuoteSearch:
    def __init__(self, crud: MongoCRUD):
        self.crud = crud
        self.crud.document_class = None

    def get_quotes(self, attr_name, attr_value):
        self.crud.document_class = Quote
        return self.crud.read_by_attr(attr_name, attr_value, count="many")

    def input_parser(self, user_input: str):
        action, k_words = None, None
        try:
            action, k_words = [el.strip() for el in user_input.split(':')]
        except ValueError:
            if user_input.strip().lower() in ["exit", "good bye", "esc"]:
                action = "exit"
        finally:
            return action, k_words

    def execute(self):
        while True:
            user_input = input("Input command (name, tag, tags, exit): \n")
            action, k_words = self.input_parser(user_input)

            attr_name = None
            attr_value = None
            match action:
                case "name":
                    self.crud.document_class = Author
                    attr_name = "author"
                    attr_value = self.crud.read_by_attr("fullname__iexact", k_words)

                case "tag":
                    attr_name = "tags__iregex"
                    attr_value = k_words

                case "tags":
                    attr_name = "tags__in"
                    attr_value = k_words.split(',')

                case "exit":
                    print("Exiting...")
                    break

                case _:
                    print("Unknown command")

            quotes = self.get_quotes(attr_name, attr_value)
            self.display_quotes(quotes)

    @staticmethod
    def display_quotes(quotes: list[Quote] | None):
        if quotes:
            for quote in quotes:
                author_name = quote.author.fullname if quote.author else "Unknown Author"
                print(f"\nАвтор: {author_name},\nЦитата: {quote.quote},\nТеги: {', '.join(quote.tags)}.\n")
        else:
            print("No quotes found")


@mongo_connection(db_name=db_name)
def main():
    radis_cache = RedisLRU(client, max_size=20)
    crud = MongoCRUD(cache=radis_cache)

    q_search = QuoteSearch(crud)
    q_search.execute()


if __name__ == '__main__':
    main()
