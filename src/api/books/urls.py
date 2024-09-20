from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.books.views import BookView

router = DefaultRouter()
router.register(r"", BookView, basename="books")

urlpatterns = [
    path("", include(router.urls)),
]
