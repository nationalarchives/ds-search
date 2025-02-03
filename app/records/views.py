from app.lib.api import ResourceNotFound
from app.records.api import record_details
from app.records.field_labels import FIELD_LABELS
from django.http import Http404, HttpResponseServerError
from django.template.response import TemplateResponse


def record_detail_view(request, iaid):
    """
    View for rendering a record's details page.
    """
    template_name = "records/record_detail.html"
    context = {"field_labels": FIELD_LABELS}

    try:
        record = record_details(iaid=iaid)
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
