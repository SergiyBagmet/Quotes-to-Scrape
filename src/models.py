from abc import abstractmethod

from faker import Faker
from mongoengine import Document, CASCADE, EmbeddedDocument
from mongoengine.fields import (
    ListField,
    StringField,
    ReferenceField,
    EmailField,
    BooleanField,
    EmbeddedDocumentField
)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=15))
    author = ReferenceField(Author, required=True, reverse_delete_rule=CASCADE)
    quote = StringField()

    meta = {"collection": "quotes_of"}


class FakerDoc(Document):
    meta = {'abstract': True}

    @staticmethod
    @abstractmethod
    def get_data_faker(fake: Faker):
        pass


class SentStatus(EmbeddedDocument):
    email_sent = BooleanField(default=False)
    sms_sent = BooleanField(default=False)


class Contact(FakerDoc):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField()
    address = StringField()
    sent_status = EmbeddedDocumentField(SentStatus, default=SentStatus())

    meta = {'collection': 'contacts'}

    @staticmethod
    def get_data_faker(fake: Faker):
        return {
            'full_name': fake.name(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'address': fake.address(),
        }


if __name__ == '__main__':
    pass
