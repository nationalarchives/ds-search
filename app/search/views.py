from app.search.api import search_records
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("search/index.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue_index(request):
    template = loader.get_template("search/catalogue/index.html")
    results = search_records(request.GET.get("q", "*"))
    context = {
        "results": results.records,
        "stats": {
            "total": results.stats_total,
            "results": results.stats_results,
        },
    }
    return HttpResponse(template.render(context, request))


def catalogue_item(request, id):
    template = loader.get_template("search/catalogue/item.html")
    context = {"id": id}
    return HttpResponse(template.render(context, request))
