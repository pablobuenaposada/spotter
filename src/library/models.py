from django.db import models
from django_extensions.db.models import TimeStampedModel


class Author(TimeStampedModel):
    name = models.CharField(max_length=100)

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)
