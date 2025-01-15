from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catalogue/", views.catalogue_index, name="catalogue"),
    path("catalogue/item.html", views.catalogue_item, name="item"),
    path("catalogue/item-no.html", views.catalogue_no, name="no"),
    path("catalogue/item-long.html", views.catalogue_long, name="no"),
    path(
        "catalogue/item-digitised.html",
        views.catalogue_item_digitised,
        name="item-digitised",
    ),
]
