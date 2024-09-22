from library.models import Book


def recommend_books(user):
    favorites = user.favorites.all()
    all_authors = [fav.book.author for fav in favorites]
    all_genres = [genre for fav in favorites for genre in fav.book.genres.all()]

    recommended_books = set()  # Use a set to avoid duplicates

    # Find books by the most common authors, excluding already favorited books
    for author in all_authors:
        similar_books = (
            Book.objects.filter(author__name=author)
            .exclude(id__in=[fav.book.id for fav in favorites])
            .order_by("-average_rating")[:20]
        )
        recommended_books.update(similar_books)

    # Find books by the most common genres, again excluding already favorited books
    for genre in all_genres:
        similar_books = (
            Book.objects.filter(genres=genre)
            .exclude(id__in=[fav.book.id for fav in favorites])
            .order_by("-average_rating")[:20]
        )
        recommended_books.update(similar_books)

    # limit the recommendations to 20 unique titles, sorted by average rating
    recommended_titles = sorted(
        recommended_books, key=lambda x: x.average_rating, reverse=True
    )[:20]

    return recommended_titles
