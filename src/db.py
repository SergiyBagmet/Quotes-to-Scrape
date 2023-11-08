from contextlib import contextmanager

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError


class MongoDB:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self.db_name = None
        self.client = None
        self.db = None

    @contextmanager
    def connection(self, db_name: str):
        self.client = None
        self.db_name = db_name
        try:
            self.client = MongoClient(self.db_uri)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            yield self.db
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except PyMongoError as e:
            print(f"An error occurred with PyMongo: {e}")
        finally:
            if self.client:
                self.client.close()

