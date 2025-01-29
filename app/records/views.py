import logging

from app.ciim.exceptions import DoesNotExist
from app.deliveryoptions.delivery_options_api import get_delivery_option
from app.deliveryoptions.utils import (
    AvailabilityCondition,
    construct_delivery_options,
)
from app.records.api import records_client
from django.http import Http404
from django.template.response import TemplateResponse

logger = logging.getLogger(__name__)


def record_detail_view(request, id):
    """
    View for rendering a record's details page.
    """
    template_name = "records/record_detail.html"
    context = {}
    page_type = "Record details page"

    try:
        # for any record
        record = records_client.get(id=id)

        if record.custom_record_type and record.custom_record_type != "CAT":
            # raise error for any other types ex ARCHON, CREATORS
            # TODO: other types ex ARCHON, CREATORS, will have their own details page templates
            raise DoesNotExist

        page_title = f"Catalogue ID: {record.iaid}"
    except DoesNotExist:
        raise Http404

    context.update(
        page_type=page_type,
        page_title=page_title,
        record=record,
    )

    # Get the delivery options for the iaid
    do_ctx = {}

    try:
        delivery_options = get_delivery_option(iaid=record.iaid)

        do_ctx = construct_delivery_options(delivery_options, record, request)

    except Exception as e:
        # Built in order exception option
        logger.warning(
            f"DORIS Connection error - returning OrderException from Availability Conditions {e.args}"
        )

        do_ctx = construct_delivery_options(
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

    context.update(do_ctx)

    return TemplateResponse(
        request=request, template=template_name, context=context
    )
