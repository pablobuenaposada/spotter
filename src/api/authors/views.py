from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.authors.serializers import AuthorSerializer
from library.models import Author


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in {"POST", "PUT", "DELETE"}:
            return [IsAuthenticated()]
        return [AllowAny()]
