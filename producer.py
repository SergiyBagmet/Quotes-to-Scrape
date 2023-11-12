from faker import Faker

from seeds import Seeder
from src.config import mongo_uri
from src.crud import MongoCRUD
from src.db import MongoDBConnection
from src.models import Contact

db_connection = MongoDBConnection(mongo_uri)
db_name = "contact_book_db"

mongo_crud = MongoCRUD()
fake = Faker()
seed = Seeder(mongo_crud, fake)


@db_connection(db_name)
def fake_contacts(count: int):
    seed.fake_to_db(Contact, count)


if __name__ == '__main__':
    # fake_contacts(10)
    pass
