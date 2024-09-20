from django.urls import include, re_path

app_name = "api"


urlpatterns = [
    re_path("authors/", include("api.authors.urls")),
    re_path("register/", include("api.register.urls")),
    re_path("login/", include("api.login.urls")),
]
