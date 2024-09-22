from rest_framework import generics, permissions
from rest_framework.response import Response

from api.books.serializers import BookOutputSerializer
from recommendations.recommendation import recommend_books


class RecommendationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookOutputSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        return Response(
            [self.get_serializer(book).data for book in recommend_books(user)]
        )
