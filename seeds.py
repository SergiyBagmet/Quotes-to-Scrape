import json
import typing as t
from bson.objectid import ObjectId
from mongoengine import Document
from src.models import Author, Quote
from src.db import MongoDBConnection
from src.crud import MongoCRUD
from src.config import mongo_uri, db_name

db_connection = MongoDBConnection(mongo_uri)


class Seeder:
    def __init__(self, crud: MongoCRUD):
        self.crud = crud

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


@db_connection(db_name=db_name)
def run_seeder():
    mongo_crud = MongoCRUD()
    seeder = Seeder(mongo_crud)
    seeder.json_to_db("start_data/authors.json", doc_cls=Author)

    seeder.json_to_db("start_data/quotes.json",
                      doc_cls=Quote,
                      ref_cls=Author,
                      ref_field='fullname',
                      data_field='author')


if __name__ == '__main__':
    run_seeder()
