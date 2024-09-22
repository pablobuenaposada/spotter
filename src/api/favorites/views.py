from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from favorite.models import Favorite

from .serializers import FavoriteSerializer


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if Favorite.objects.filter(
            user=self.request.user, book=serializer.validated_data["book"]
        ).exists():
            raise ValidationError("This book is already marked as favorite")
        serializer.save(user=self.request.user)


class FavoriteDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
