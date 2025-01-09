from app.ciim.exceptions import DoesNotExist
from app.records.api import records_client
from django.shortcuts import Http404
from django.template.response import TemplateResponse
from app.deliveryoptions.delivery_options_api import get_delivery_option
from app.deliveryoptions.utils import (
    AvailabilityCondition,
    construct_delivery_options,
)


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

        page_title = f"Catalogue ID: {record.iaid}"
    except DoesNotExist:
        raise Http404
    
    context.update(
        page_type=page_type,
        page_title=page_title,
    )

    # Get the delivery options for the iaid
    do_ctx = {}

    try:
        delivery_options = get_delivery_option(iaid=record.iaid)
        

        do_ctx = construct_delivery_options(delivery_options, record)
    except Exception as e:
        # Built in order exception option
        do_ctx = construct_delivery_options(
            [
                {
                    "options": AvailabilityCondition.OrderException,
                    "surrogateLinks": [],
                    "advancedOrderUrlParameters": "",
                }
            ],
            record,
        )
        do_ctx['do_exception'] = f"Unexpected {e=}, {type(e)=}"

    context.update(do_ctx)

    return TemplateResponse(
        request=request, template=template_name, context=context
    )
