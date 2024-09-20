import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from model_bakery import baker

from library.models import Author, Book


@pytest.mark.django_db
class TestAuthor:
    def test_mandatory_fields(self):
        with pytest.raises(ValidationError) as error:
            Author.objects.create()
        assert list(error.value.error_dict.keys()) == ["name"]

    def test_valid(self):
        author = baker.make(Author)
        expected = {
            "id": author.id,
            "created": author.created,
            "modified": author.modified,
            "name": author.name,
        }
        for field in {field.name for field in Author._meta.get_fields()} - {"books"}:
            assert getattr(author, field) == expected[field]


@pytest.mark.django_db
class TestBook:
    def test_mandatory_fields(self):
        with pytest.raises(IntegrityError) as error:
            Book.objects.create()

        assert (
            'null value in column "title" of relation "library_book" violates not-null constraint'
            in str(error.value)
        )

    def test_valid(self):
        book = baker.make(Book, title="foo", author=baker.make(Author))
        expected = {
            "id": book.id,
            "created": book.created,
            "modified": book.modified,
            "title": book.title,
            "author": book.author,
        }
        for field in {field.name for field in Book._meta.get_fields()}:
            assert getattr(book, field) == expected[field]
