from django.urls import include, re_path

app_name = "api"


urlpatterns = [
    re_path("authors/", include("api.authors.urls")),
    re_path("books/", include("api.books.urls")),
    re_path("favorites/", include("api.favorites.urls")),
    re_path("recommendations/", include("api.recommendations.urls")),
    re_path("register/", include("api.register.urls")),
    re_path("login/", include("api.login.urls")),
]
