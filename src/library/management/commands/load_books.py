import json
import time

from django.core.management.base import BaseCommand
from django.db import IntegrityError, connection

from library.models import Author, Book, Genre

LIMIT = 1000


class Command(BaseCommand):
    help = "Load books from a JSON file"

    def handle(self, *args, **kwargs):
        start_time = time.time()
        count = 0

        with open("loader/books.json", "r") as file:
            for _, line in enumerate(file, start=1):
                if count >= LIMIT:
                    break

                book_data = json.loads(line)
                if "author_name" in book_data:
                    author, _ = Author.objects.get_or_create(
                        id=book_data["author_id"],
                        defaults={"name": book_data["author_name"]},
                    )
                else:
                    author, _ = Author.objects.get_or_create(
                        id=book_data["authors"][0]["id"],
                        defaults={"name": book_data["authors"][0]["name"]},
                    )

                try:
                    book, _ = Book.objects.get_or_create(
                        id=book_data["id"],
                        defaults={
                            "title": book_data["title"][:199],
                            "author": author,
                            "average_rating": book_data["average_rating"],
                        },
                    )
                except IntegrityError:
                    pass
                else:
                    if "shelves" in book_data:
                        for shelf in book_data["shelves"]:
                            genre_name = shelf["name"]
                            genre, _ = Genre.objects.get_or_create(name=genre_name)
                            book.genres.add(genre)

                count += 1

        # reset the primary key sequence
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval('library_book_id_seq', (SELECT MAX(id) FROM library_book));"
            )

        end_time = time.time()
        elapsed_time = end_time - start_time

        self.stdout.write(
            self.style.SUCCESS(
                f"Books and authors populated successfully in {elapsed_time:.2f} seconds!"
            )
        )
