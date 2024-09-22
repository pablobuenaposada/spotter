from rest_framework import serializers

from library.models import Book, Genre


class BookOutputSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Genre.objects.all()
    )

    class Meta:
        model = Book
        fields = "__all__"


class BookInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
