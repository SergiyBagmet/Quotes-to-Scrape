import os
import sys

from pika import BlockingConnection

from producer import exchange, queue_args
from src.config import mongo_uri, connection_rmq
from src.crud import MongoCRUD
from src.db import MongoDBConnection
from src.models import Contact

db_connection = MongoDBConnection(mongo_uri)
db_name = "contact_db"

contact_crud = MongoCRUD(Contact)


@db_connection(db_name)
def consumer_contacts(connection: BlockingConnection, crud: MongoCRUD, exchange_name: str, queue_field: dict[str]):
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    def callback(ch, method, properties, body):
        message = body.decode()
        send_key = queue_field.get(method.routing_key)
        send_attr = f"{send_key}_sent"
        contact = crud.read(message)
        if contact is not None:
            print(f" [x] Send {send_key} to  {contact.full_name}")
            crud.update_send_status(contact.id, send_attr, True)

        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    for queue, field in queue_field.items():
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        consumer_contacts(connection_rmq, contact_crud, exchange, queue_args)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
