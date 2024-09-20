from django.urls import include, re_path

app_name = "api"


urlpatterns = [
    re_path("authors/", include("api.authors.urls")),
]