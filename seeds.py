import json
import typing as t

from mongoengine import Document
from faker import Faker

from src.models import Author, Quote, FakerDoc
from src.db import MongoDBConnection
from src.crud import MongoCRUD
from src.config import mongo_uri, db_name
from my_logger import MyLogger

logger_seed = MyLogger('seed', 10).get_logger()

db_connection = MongoDBConnection(mongo_uri)


class Seeder:
    def __init__(self, crud: MongoCRUD, fake: Faker | None = None):
        self.crud = crud
        self.fake = fake if fake is not None else None

    def fake_to_db(self, doc_cls: t.Type[FakerDoc]) -> Document:
        self.crud.document_class = doc_cls
        return self.crud.create(doc_cls.get_data_faker(self.fake))

    def json_to_db(self,
                   json_path,
                   doc_cls: t.Type[Document],
                   ref_cls: t.Type[Document] | None = None,
                   ref_field: str | None = None,
                   data_field: str | None = None,
                   ):

        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for el in data:
            if ref_cls:
                self.crud.document_class = ref_cls
                doc = self.crud.read_by_attr(ref_field, el[data_field])
                el[data_field] = doc

            self.crud.document_class = doc_cls
            self.crud.create(el)
        logger_seed.info(f"Saving json {json_path} by documents '{self.crud.document_class}' to DB")


@db_connection(db_name=db_name)
def run_seeder(crud: MongoCRUD, authors_json, quotes_json):

    seeder = Seeder(crud)
    seeder.json_to_db(authors_json, doc_cls=Author)
    seeder.json_to_db(quotes_json,
                      doc_cls=Quote,
                      ref_cls=Author,
                      ref_field='fullname',
                      data_field='author')


if __name__ == '__main__':
    pass
