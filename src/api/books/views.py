from elasticsearch_dsl import Q
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.books.serializers import BookSerializer
from library.documents import BookDocument
from library.models import Book


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in {"POST", "PUT", "DELETE"}:
            return [IsAuthenticated()]
        return [AllowAny()]


class BookSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        if query:
            search = BookDocument.search()
            search = search.query(
                Q("multi_match", query=query, fields=["title", "author.name"])
            )
            results = search.execute()
            return Response(
                [
                    {"id": int(hit.meta.id), "title": hit.title, "author": hit.author}
                    for hit in results
                ]
            )
        return Response(
            {"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST
        )
