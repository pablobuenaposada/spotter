from django.db import models
from django_extensions.db.models import TimeStampedModel


class Author(TimeStampedModel):
    name = models.CharField(max_length=100)

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Book(TimeStampedModel):
    title = models.CharField(max_length=200, null=False, blank=False, default=None)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    average_rating = models.FloatField()
    genres = models.ManyToManyField(Genre)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_book_author"
            )
        ]
