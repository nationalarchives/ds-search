from app.search import views
from django.urls import path

urlpatterns = [
    path("search/", views.CatalogueSearchView.as_view(), name="catalogue"),
]
