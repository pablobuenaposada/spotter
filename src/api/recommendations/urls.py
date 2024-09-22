from django.urls import path

from .views import RecommendationListView

urlpatterns = [
    path("", RecommendationListView.as_view(), name="recommendations"),
]
