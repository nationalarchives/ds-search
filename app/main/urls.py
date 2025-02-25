from app.main import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("cookies/", views.cookies, name="cookies"),
]
