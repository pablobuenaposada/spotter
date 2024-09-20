from unittest.mock import ANY

import pytest
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
class TestsLogin:
    def endpoint(self):
        return resolve_url("api:login")

    def test_url(self):
        assert self.endpoint() == "/api/login/"

    def test_success(self, client):
        password = "whatever"
        user = baker.make(User)
        user.set_password(password)
        user.save()

        response = client.post(
            self.endpoint(), {"username": user.username, "password": password}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"access": ANY}

    def test_user_does_not_exist(self, client):
        response = client.post(
            self.endpoint(), {"username": "foo", "password": "whatever"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "Invalid credentials"}
