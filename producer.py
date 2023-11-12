import json

from pika import BlockingConnection
from faker import Faker

from seeds import Seeder
from src.config import mongo_uri, connection_rmq
from src.crud import MongoCRUD
from src.db import MongoDBConnection
from src.models import Contact

db_connection = MongoDBConnection(mongo_uri)
db_name = "contact_db"

mongo_crud = MongoCRUD()
fake = Faker()
seed = Seeder(mongo_crud, fake)


@db_connection(db_name)
def producer_contacts(connection: BlockingConnection, count: int, exchange_name: str, queue_names: list[str]):

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    for queue_name in queue_names:
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name)

    for _ in range(count):
        contact = seed.fake_to_db(Contact)
        message = str(contact.id).encode('utf-8')

        for queue_name in queue_names:
            channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=message)
            print(f" [x] queue[{queue_name}] Sent: {message}")

    channel.close()


if __name__ == '__main__':
    producer_contacts(connection_rmq, 10, "Senders", ["email_queue", "sms_queue"])
