from django.urls import path

from api.login import views

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
]
