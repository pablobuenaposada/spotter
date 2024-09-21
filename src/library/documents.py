from django_elasticsearch_dsl import Index, fields
from django_elasticsearch_dsl.documents import DocType

from library.models import Book

BOOK_INDEX_NAME = "book"
book = Index(BOOK_INDEX_NAME)


@book.doc_type
class BookDocument(DocType):
    author = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
        }
    )

    class Django:
        model = Book
        fields = ["title"]
