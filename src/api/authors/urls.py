from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.authors.views import AuthorView

router = DefaultRouter()
router.register(r"", AuthorView, basename="authors")

urlpatterns = [
    path("", include(router.urls)),
]
