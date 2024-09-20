from rest_framework import viewsets

from api.authors.serializers import AuthorSerializer
from library.models import Author


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
