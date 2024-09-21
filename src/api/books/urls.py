from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.books import views
from api.books.views import BookView

router = DefaultRouter()
router.register(r"", BookView, basename="books")

urlpatterns = [
    path("", include(router.urls)),
    path("search", views.BookSearchView.as_view(), name="books-search"),
]
