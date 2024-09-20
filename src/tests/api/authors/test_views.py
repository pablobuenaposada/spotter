import pytest
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status

from api.authors.serializers import AuthorSerializer
from library.models import Author


@pytest.mark.django_db
class TestsAuthorViewDetail:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.author = baker.make(Author)

    def endpoint(self, pk):
        return resolve_url("api:authors-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.author.id) == f"/api/authors/{self.author.id}/"

    def test_success(self, client):
        response = client.get(self.endpoint(self.author.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == AuthorSerializer(self.author).data


@pytest.mark.django_db
class TestsAuthorViewList:
    def endpoint(self):
        return resolve_url("api:authors-list")

    def test_url(self):
        assert self.endpoint() == "/api/authors/"

    def test_success(self, client):
        authors = baker.make(Author, _quantity=2)
        response = client.get(self.endpoint())

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [AuthorSerializer(author).data for author in authors]


@pytest.mark.django_db
class TestsAuthorViewCreate:
    def endpoint(self):
        return resolve_url("api:authors-list")

    def test_url(self):
        assert self.endpoint() == "/api/authors/"

    def test_success(self, client):
        assert Author.objects.exists() is False

        data = {"name": "Santiago Segura"}
        response = client.post(self.endpoint(), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == AuthorSerializer(Author.objects.get()).data

    def test_invalid_data(self, client):
        """Wrong payload should return 400 status code"""
        data = {}
        response = client.post(self.endpoint(), data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestsAuthorViewUpdate:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.author = baker.make(Author)

    def endpoint(self, pk):
        return resolve_url("api:authors-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.author.pk) == f"/api/authors/{self.author.pk}/"

    def test_success(self, client):
        data = {"name": "foo"}
        response = client.put(
            self.endpoint(self.author.pk), data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == AuthorSerializer(Author.objects.get()).data

        self.author.refresh_from_db()
        assert self.author.name == data["name"]


@pytest.mark.django_db
class TestsAuthorViewDelete:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.author = baker.make(Author)

    def endpoint(self, pk):
        return resolve_url("api:authors-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.author.pk) == f"/api/authors/{self.author.pk}/"

    def test_success(self, client):
        assert Author.objects.filter(id=self.author.pk).exists() is True

        response = client.delete(self.endpoint(self.author.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Author.objects.exists() is False

    def test_not_found(self, client):
        """Trying to delete an author that doesn't exist"""
        invalid_id = self.author.pk + 1
        response = client.delete(self.endpoint(invalid_id))

        assert response.status_code == status.HTTP_404_NOT_FOUND
