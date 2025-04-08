import logging
import os

from app.deliveryoptions.api import delivery_options_request_handler
from app.deliveryoptions.delivery_options import (
    AvailabilityCondition,
    construct_delivery_options,
)
from app.lib.api import ResourceNotFound
from app.records.api import record_details_by_id
from app.records.labels import FIELD_LABELS
from django.http import Http404
from django.template.response import TemplateResponse
from sentry_sdk import capture_message

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

logger = logging.getLogger(__name__)


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

    determine_delivery_options = True

    if record.custom_record_type:
        if record.custom_record_type == "ARCHON":
            determine_delivery_options = False
            template_name = "records/archon_detail.html"
        if record.custom_record_type == "CREATORS":
            template_name = "records/creator_detail.html"
            determine_delivery_options = False

    if determine_delivery_options:
        # Only get the delivery options if we are looking at records
        # Get the delivery options for the iaid
        delivery_options_context = {}

        try:
            delivery_options = delivery_options_request_handler(
                iaid=record.iaid
            )

            delivery_options_context = construct_delivery_options(
                delivery_options, record, request
            )

        except Exception as e:
            # Built in order exception option
            error_message = f"DORIS Connection error using url '{os.getenv("DELIVERY_OPTIONS_API_URL", "")}' - returning OrderException from Availability Conditions {str(e)}"

            # Sentry notification
            logger.error(error_message)
            capture_message(error_message)

            # The delivery options include a special case called OrderException which has nothing to do with
            # python exceptions. It is the message to be displayed when the connection is down or there is no
            # match for the given iaid. So, we don't treat it as a python exception beyond this point.
            delivery_options_context = construct_delivery_options(
                [
                    {
                        "options": AvailabilityCondition.OrderException,
                        "surrogateLinks": [],
                        "advancedOrderUrlParameters": "",
                    }
                ],
                record,
                request,
            )

        context.update(delivery_options_context)

    return TemplateResponse(
        request=request, template=template_name, context=context
    )
