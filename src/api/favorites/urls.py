from django.urls import path

from .views import FavoriteDeleteView, FavoriteListCreateView

urlpatterns = [
    path("", FavoriteListCreateView.as_view(), name="favorite-list-create"),
    path("<int:pk>/", FavoriteDeleteView.as_view(), name="favorite-delete"),
]
