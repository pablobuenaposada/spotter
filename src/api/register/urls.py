from django.urls import path

from api.register import views

urlpatterns = [
    path("", views.RegisterView.as_view(), name="register"),
]
