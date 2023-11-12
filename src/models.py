from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField, EmailField, BooleanField, DictField


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


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField()
    address = StringField()

    sent_status = DictField(default={'email_sent': False, 'sms_sent': False})

    meta = {'collection': 'contacts'}
