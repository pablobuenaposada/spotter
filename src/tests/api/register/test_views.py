import pytest
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from rest_framework import status

from api.register.serializers import UserSerializer


@pytest.mark.django_db
class TestsRegister:
    def endpoint(self):
        return resolve_url("api:register")

    def test_url(self):
        assert self.endpoint() == "/api/register/"

    def test_success(self, client):
        assert User.objects.exists() is False

        data = {"username": "foo", "password": "bar"}
        response = client.post(self.endpoint(), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == UserSerializer(User.objects.get()).data
