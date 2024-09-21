import json

import pytest
from django.core import management
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status

from api.books.serializers import BookSerializer
from library.models import Author, Book


@pytest.mark.django_db
class TestsBookViewDetail:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.book = baker.make(Book, title="foo")

    def endpoint(self, pk):
        return resolve_url("api:books-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.book.id) == f"/api/books/{self.book.id}/"

    def test_success(self, client):
        response = client.get(self.endpoint(self.book.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == BookSerializer(self.book).data


@pytest.mark.django_db
class TestsBookViewList:
    def endpoint(self):
        return resolve_url("api:books-list")

    def test_url(self):
        assert self.endpoint() == "/api/books/"

    def test_success(self, client):
        books = baker.make(Book, title="foo", _quantity=2)
        response = client.get(self.endpoint())

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [BookSerializer(book).data for book in books]


@pytest.mark.django_db
class TestsBookViewCreate:
    def endpoint(self):
        return resolve_url("api:books-list")

    def test_url(self):
        assert self.endpoint() == "/api/books/"

    def test_success(self, authenticated_client):
        assert Book.objects.exists() is False

        author = baker.make(Author)
        data = {"title": "Never ending story", "author": author.id}
        response = authenticated_client.post(self.endpoint(), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == BookSerializer(Book.objects.get()).data

    def test_invalid_data(self, authenticated_client):
        """Wrong payload should return 400 status code"""
        data = {}
        response = authenticated_client.post(self.endpoint(), data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestsBookViewUpdate:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.book = baker.make(Book, title="foo")

    def endpoint(self, pk):
        return resolve_url("api:books-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.book.pk) == f"/api/books/{self.book.pk}/"

    def test_success(self, authenticated_client):
        data = {"title": "foo bar", "author": self.book.author.id}
        response = authenticated_client.put(
            self.endpoint(self.book.pk),
            json.dumps(data),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == BookSerializer(Book.objects.get()).data

        self.book.refresh_from_db()
        assert self.book.title == data["title"]


@pytest.mark.django_db
class TestsBookViewDelete:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.book = baker.make(Book, title="foo")

    def endpoint(self, pk):
        return resolve_url("api:books-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.book.pk) == f"/api/books/{self.book.pk}/"

    def test_success(self, authenticated_client):
        assert Book.objects.filter(id=self.book.pk).exists() is True

        response = authenticated_client.delete(self.endpoint(self.book.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.exists() is False

    def test_not_found(self, authenticated_client):
        """Trying to delete a book that doesn't exist"""
        invalid_id = self.book.pk + 1
        response = authenticated_client.delete(self.endpoint(invalid_id))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestsBookSearchView:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.book1 = baker.make(
            Book, title="foo", author=baker.make(Author, name="Jhon")
        )
        self.book2 = baker.make(
            Book, title="bar", author=baker.make(Author, name="Monica")
        )
        self.book3 = baker.make(
            Book, title="banana", author=baker.make(Author, name="Ryan")
        )

    def endpoint(self):
        return resolve_url("api:books-search")

    def test_url(self):
        assert self.endpoint() == "/api/books/search"

    def test_success(self, client):
        # clean elasticsearch indexes
        management.call_command("search_index", "--delete", "-f")
        management.call_command("search_index", "--rebuild", "-f")

        # match by title
        response = client.get(self.endpoint(), data={"q": "foo"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": self.book1.id,
                "title": self.book1.title,
                "author": {"id": self.book1.author.id, "name": self.book1.author.name},
            }
        ]

        # match by author
        response = client.get(self.endpoint(), data={"q": "monica"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": self.book2.id,
                "title": self.book2.title,
                "author": {"id": self.book2.author.id, "name": self.book2.author.name},
            }
        ]

        # match by title and author
        response = client.get(self.endpoint(), data={"q": "foo monica"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": self.book1.id,
                "title": self.book1.title,
                "author": {"id": self.book1.author.id, "name": self.book1.author.name},
            },
            {
                "id": self.book2.id,
                "title": self.book2.title,
                "author": {"id": self.book2.author.id, "name": self.book2.author.name},
            },
        ]
