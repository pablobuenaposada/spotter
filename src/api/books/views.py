from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.books.serializers import BookSerializer
from library.models import Book


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in {"POST", "PUT", "DELETE"}:
            return [IsAuthenticated()]
        return [AllowAny()]
