from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from library.models import Book


class Favorite(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "book")
