from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catalogue/", views.catalogue_index, name="catalogue"),
]
