from app.search import views
from django.urls import path

urlpatterns = [
    path("search/", views.catalogue_search_view, name="catalogue"),
]
