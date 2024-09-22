from elasticsearch_dsl import Q
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.books.serializers import BookInputSerializer, BookOutputSerializer
from library.documents import BookDocument
from library.models import Book


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.request.method in {"POST", "PUT", "DELETE"}:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in {"POST", "PUT", "PATCH"}:
            return BookInputSerializer
        return BookOutputSerializer


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
                    BookOutputSerializer(Book.objects.get(id=hit.meta.id)).data
                    for hit in results
                ]
            )
        return Response(
            {"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST
        )
