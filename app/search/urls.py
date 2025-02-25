from app.search import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("catalogue/", views.catalogue_index, name="catalogue"),
]
