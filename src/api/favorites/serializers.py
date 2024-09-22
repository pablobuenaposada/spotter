from rest_framework import serializers

from favorite.models import Favorite
from library.models import Book


class FavoriteSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Favorite
        fields = ["id", "user", "book"]
        read_only_fields = ["user"]
