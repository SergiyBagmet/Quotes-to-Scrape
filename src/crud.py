import typing as t
from functools import wraps

from redis_lru import RedisLRU
from bson.objectid import ObjectId
from mongoengine import Document, DoesNotExist


class MongoCRUD:
    def __init__(self,
                 document_class: t.Type[Document] | None = None,
                 cache: t.Optional[RedisLRU] = None
                 ):

        self.document_class = document_class
        self.cache = cache

    @staticmethod
    def cache_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.cache:
                return self.cache(func)(self, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @property
    def document_class(self) -> t.Type[Document]:
        return self._document_class

    @document_class.setter
    def document_class(self, new_document_class: t.Type[Document] | None):
        if new_document_class and not issubclass(new_document_class, Document):
            pass
            raise TypeError("new_document_class must be a subclass of mongoengine.Document")
        self._document_class = new_document_class

    def create(self, document_data: dict):
        new_document = self.document_class(**document_data)
        new_document.save()
        return new_document

    @cache_decorator
    def read(self, pk: ObjectId):
        try:
            document = self.document_class.objects.get(id=pk)
            return document
        except DoesNotExist:
            return None

    @cache_decorator
    def read_by_attr(self, attr_name: str, value: str, count: str = 'one'):
        doc = None
        try:
            if count == 'one':
                doc = self.document_class.objects.get(**{attr_name: value})
            elif count == 'many':
                doc = self.document_class.objects.filter(**{attr_name: value})
            return doc
        except DoesNotExist:
            return None

    def read_all(self):
        return self.document_class.objects.all()

    def update(self, pk: ObjectId, document_data: dict):
        try:
            document: Document = self.document_class.objects.get(id=pk)
            document.update(**document_data)
            return document
        except DoesNotExist:
            return None

    def update_send_status(self, pk: ObjectId, send_key: str, status: bool):
        try:
            document: Document = self.document_class.objects.get(id=pk)
            if document and hasattr(document, 'sent_status'):
                document.update(**{f'set__sent_status__{send_key}': status})
                return document
        except DoesNotExist:
            return None

    def delete(self, pk: ObjectId):
        try:
            document: Document = self.document_class.objects.get(id=pk)
            document.delete()
            return document
        except DoesNotExist:
            return None
