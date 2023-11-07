from mongoengine import Document
from mongoengine.fields import ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField(max_length=300)
    
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Author, required=True)
    quote = StringField(max_length=300, required=True)
    
    meta = {"collection": "quotes_of"}
