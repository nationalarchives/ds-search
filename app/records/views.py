from app.lib.api import ResourceNotFound
from app.records.api import record_details_by_id
from app.records.labels import FIELD_LABELS
from django.http import Http404
from django.template.response import TemplateResponse

# TODO: Implement record_detail_by_reference once Rosetta has support
# from app.records.api import record_details_by_ref
# from django.template.loader import get_template
# from django.urls import reverse
# def record_detail_by_reference(request, reference):
#     """
#     View for rendering a record's details page.
#     """
#     template_name = "records/record_detail.html"
#     context = {"field_labels": FIELD_LABELS, "level_labels": LEVEL_LABELS, "non_tna_level_labels": NON_TNA_LEVEL_LABELS}

#     try:
#         # record = record_details_by_ref(id=reference)
#         record = record_details_by_id(id="D4664016")
#     except ResourceNotFound:
#         raise Http404
#     except Exception:
#         raise HttpResponseServerError

#     context.update(
#         record=record,
#         canonical=reverse(
#             "details-page-machine-readable", kwargs={"id": record.id}
#         ),
#     )

#     if record.custom_record_type:
#         if record.custom_record_type == "ARCHON":
#             template_name = "records/archon_detail.html"
#         if record.custom_record_type == "CREATORS":
#             template_name = "records/creator_detail.html"

#     return TemplateResponse(
#         request=request, template=template_name, context=context
#     )


def record_detail_view(request, id):
    """
    View for rendering a record's details page.
    """
    template_name = "records/record_detail.html"
    context: dict = {
        "field_labels": FIELD_LABELS,
    }

    try:
        record = record_details_by_id(id=id)
    except ResourceNotFound:
        raise Http404
    except Exception as e:
        context = {"exception_message": str(e)}
        return TemplateResponse(
            request=request,
            template="errors/server_error.html",
            context=context,
            status=502,
        )

    context.update(
        record=record,
    )

    if record.custom_record_type:
        if record.custom_record_type == "ARCHON":
            template_name = "records/archon_detail.html"
        if record.custom_record_type == "CREATORS":
            template_name = "records/creator_detail.html"

    return TemplateResponse(
        request=request, template=template_name, context=context
    )
