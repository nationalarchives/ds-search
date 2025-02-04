from app.lib.api import ResourceNotFound
from app.records.api import record_details_by_iaid, record_details_by_ref
from app.records.labels import FIELD_LABELS, LEVEL_LABELS
from django.http import Http404, HttpResponseServerError
from django.template.response import TemplateResponse
from django.urls import reverse


def record_detail_by_reference(request, reference):
    """
    View for rendering a record's details page.
    """
    template_name = "records/record_detail.html"
    context = {"field_labels": FIELD_LABELS, "level_labels": LEVEL_LABELS}

    try:
        # record = record_details_by_ref(iaid=reference)
        record = record_details_by_iaid(iaid="D4664016")
    except ResourceNotFound:
        raise Http404
    except Exception:
        raise HttpResponseServerError

    context.update(
        record=record,
        canonical=reverse(
            "details-page-machine-readable", kwargs={"iaid": record.iaid}
        ),
    )

    if record.custom_record_type and record.custom_record_type != "CAT":
        # raise error for any other types ex ARCHON, CREATORS
        # TODO: other types ex ARCHON, CREATORS, will have their own details page templates
        raise Http404

    return TemplateResponse(
        request=request, template=template_name, context=context
    )


def record_detail_view(request, iaid):
    """
    View for rendering a record's details page.
    """
    template_name = "records/record_detail.html"
    context = {"field_labels": FIELD_LABELS, "level_labels": LEVEL_LABELS}

    try:
        record = record_details_by_iaid(iaid=iaid)
    except ResourceNotFound:
        raise Http404
    except Exception:
        raise HttpResponseServerError

    context.update(
        record=record,
    )

    if record.custom_record_type and record.custom_record_type != "CAT":
        # raise error for any other types ex ARCHON, CREATORS
        # TODO: other types ex ARCHON, CREATORS, will have their own details page templates
        raise Http404

    return TemplateResponse(
        request=request, template=template_name, context=context
    )
