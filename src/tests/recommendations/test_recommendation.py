import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from favorite.models import Favorite
from library.models import Author, Book, Genre
from recommendations.recommendation import recommend_books


@pytest.mark.django_db
class TestRecommendBooks:
    def test_success(self):
        user = baker.make(User)

        # Harry Potter saga
        author1 = baker.make(Author, name="J. K. Rowling")
        genre1 = baker.make(Genre, name="Fantasy")
        genre2 = baker.make(Genre, name="Adventure")
        book1 = baker.make(
            Book,
            title="Harry Potter Philosopher's Stone",
            author=author1,
            average_rating=1,
        )
        book1.genres.set([genre1, genre2])
        book2 = baker.make(
            Book,
            title="Harry Potter Chamber of Secrets",
            author=author1,
            average_rating=2,
        )
        book2.genres.set([genre1, genre2])
        book3 = baker.make(
            Book,
            title="Harry Potter Prisoner of Azkaban",
            author=author1,
            average_rating=4,
        )
        book3.genres.set([genre1, genre2])

        # this book will not match us, not the author neither the genre
        author2 = baker.make(Author, name="Gabriel García Márquez")
        genre3 = baker.make(Genre, name="Novel")
        book4 = baker.make(
            Book,
            title="One Hundred Years of Solitude",
            author=author2,
            average_rating=5,
        )
        book4.genres.set([genre3])

        # will match the genre
        author3 = baker.make(Author, name="Miguel de Cervantes")
        book5 = baker.make(Book, title="Don Quixote", author=author3, average_rating=3)
        book5.genres.set([genre2])

        baker.make(
            Favorite, user=user, book=book1
        )  # we like Harry Potter, adventure and fantasy

        assert recommend_books(user) == [book3, book5, book2]
