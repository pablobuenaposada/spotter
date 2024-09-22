import pytest
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status

from api.favorites.serializers import FavoriteSerializer
from favorite.models import Favorite
from library.models import Book


@pytest.mark.django_db
class TestsFavoriteDetailView:
    def endpoint(self):
        return resolve_url("api:favorite-list-create")

    def test_url(self):
        assert self.endpoint() == "/api/favorites/"

    def test_success(self, authenticated_client):
        book = baker.make(Book, title="foo")
        favorite = baker.make(Favorite, book=book, user=User.objects.get())
        response = authenticated_client.get(self.endpoint())

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [FavoriteSerializer(favorite).data]
