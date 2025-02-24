from app.search.api import search_records
from django.http import HttpResponse
from django.template import loader


def catalogue_search_view(request):
    template = loader.get_template("search/catalogue.html")
    results = search_records(request.GET.get("q", None))
    context = {
        "results": results.records,
        "stats": {
            "total": results.stats_total,
            "results": results.stats_results,
        },
    }
    return HttpResponse(template.render(context, request))
