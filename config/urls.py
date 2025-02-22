"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from app.errors import views as errors_view
from app.records import converters
from app.records import views as records_views
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, register_converter

register_converter(converters.IDConverter, "id")

handler404 = "app.errors.views.page_not_found_error_view"

urlpatterns = [
    path("", include(("app.main.urls", "main"), namespace="main")),
    path("healthcheck/", include("app.healthcheck.urls")),
    path(
        r"catalogue/id/<id:id>/",
        records_views.record_detail_view,
        name="details-page-machine-readable",
    ),
    # TODO: Implement record_details_by_ref once Rosetta has support
    # path(
    #     r"catalogue/ref/<path:reference>/",
    #     records_views.record_detail_by_reference,
    # ),
    path(
        "search/",
        include(("app.search.urls", "search"), namespace="search"),
    ),
    path(
        r"404/",
        errors_view.page_not_found_error_view,
    ),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if apps.is_installed("debug_toolbar"):
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns
