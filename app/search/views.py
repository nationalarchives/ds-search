from app.errors import views as errors_view
from app.lib.api import ResourceNotFound
from app.search.api import search_records
from django.http import HttpResponse
from django.template import loader


def catalogue_search_view(request):
    template = loader.get_template("search/catalogue.html")
    results_per_page = 20
    page = int(request.GET.get("page", 1))
    try:
        results = search_records(
            query=request.GET.get("q", None),
            results_per_page=results_per_page,
            page=page,
        )
    except ResourceNotFound:
        return HttpResponse(template.render({}, request))
    results_range = {
        "from": ((page - 1) * results_per_page) + 1,
        "to": ((page - 1) * results_per_page) + results.stats_results,
    }
    print(results_range["to"])
    print(results.stats_total)
    if results_range["to"] > results.stats_total:
        return errors_view.page_not_found_error_view(request=request)
    context = {
        "results": results.records,
        "results_per_page": results_per_page,
        "page": page,
        "results_range": results_range,
        "stats": {
            "total": results.stats_total,
            "results": results.stats_results,
        },
    }
    return HttpResponse(template.render(context, request))
