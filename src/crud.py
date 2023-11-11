import typing as t

from bson.objectid import ObjectId
from mongoengine import Document, DoesNotExist


class MongoCRUD:
    def __init__(self, document_class: t.Type[Document] | None = None):
        self.document_class = document_class

    @property
    def document_class(self) -> t.Type[Document]:
        return self._document_class

    @document_class.setter
    def document_class(self, new_document_class: t.Type[Document] | None):
        if new_document_class and not issubclass(new_document_class, Document):
            raise TypeError("new_document_class must be a subclass of mongoengine.Document")
        self._document_class = new_document_class

    def create(self, document_data: dict):
        new_document = self.document_class(**document_data)
        new_document.save()
        return new_document

    def read(self, pk: ObjectId):
        try:
            document = self.document_class.objects.get(id=pk)
            return document
        except DoesNotExist:
            return None

    def read_by_attr(self, attr_name: str, value: str):
        try:
            document = self.document_class.objects.get(**{attr_name: value})
            return document
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

    def delete(self, pk: ObjectId):
        try:
            document: Document = self.document_class.objects.get(id=pk)
            document.delete()
            return document
        except DoesNotExist:
            return None
