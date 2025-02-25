from app.records import views
from django.urls import path

urlpatterns = [
    path(
        r"id/<id:id>/",
        views.record_detail_view,
        name="details",
    ),
    path(
        r"id/<id:id>/related/",
        views.related_records_view,
        name="related",
    ),
    path(
        r"id/<id:id>/help/",
        views.records_help_view,
        name="help",
    ),
    # TODO: Implement record_details_by_ref once Rosetta has support
    # path(
    #     r"ref/<path:reference>/",
    #     views.record_detail_by_reference,
    # ),
]
