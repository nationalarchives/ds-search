import math

from app.errors import views as errors_view
from app.lib.api import ResourceNotFound
from app.lib.pagination import pagination_object
from app.search.api import search_records
from django.http import HttpResponse
from django.template import loader


def catalogue_search_view(request):
    template = loader.get_template("search/catalogue.html")
    results_per_page = 20
    page = int(request.GET.get("page", 1))
    sort_order = request.GET.get("sort", "")
    sort = sort_order.split(":")[0] if sort_order else ""
    order = sort_order.split(":")[1] if sort_order else ""
    try:
        results = search_records(
            query=request.GET.get("q", None),
            results_per_page=results_per_page,
            page=page,
            sort=sort,
            order=order,
        )
    except ResourceNotFound:
        return HttpResponse(template.render({}, request))
    results_range = {
        "from": ((page - 1) * results_per_page) + 1,
        "to": ((page - 1) * results_per_page) + results.stats_results,
    }
    pages = math.ceil(results.stats_total / results_per_page)
    if pages > 500:
        pages = 500
    if page > pages:
        return errors_view.page_not_found_error_view(request=request)
    context = {
        "results": results.records,
        "results_range": results_range,
        "stats": {
            "total": results.stats_total,
            "results": results.stats_results,
        },
        "pagination": pagination_object(page, pages, request.GET),
    }
    return HttpResponse(template.render(context, request))
