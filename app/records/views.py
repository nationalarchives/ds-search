from django.shortcuts import Http404
from django.template.response import TemplateResponse


def record_detail_view(request, id):
    """
    View for rendering a record's details page.
    """
    template_name = "records/record_detail.html"
    context = {}
    page_type = "Record details page"

    page_title = f"Catalogue ID: {id}"

    context.update(
        page_type=page_type,
        page_title=page_title,
    )

    return TemplateResponse(
        request=request, template=template_name, context=context
    )
