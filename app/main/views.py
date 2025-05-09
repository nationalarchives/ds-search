from app.lib.api import JSONAPIClient
from django.conf import settings
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("main/index.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue(request):
    template = loader.get_template("main/catalogue.html")
    context = {}

    client = JSONAPIClient(settings.WAGTAIL_API_URL)
    client.add_parameters(
        {
            "child_of": settings.WAGTAIL_EXPLORE_THE_COLLECTION_PAGE_ID,
            "limit": 3,
            "order": "-first_published_at",
        }
    )
    response_data = client.get("/pages/")
    context["pages"] = response_data.get("items", [])

    client.add_parameters(
        {
            "child_of": settings.WAGTAIL_HOME_PAGE_ID,
            "limit": 3,
            "order": "-first_published_at",
        }
    )
    response_data = client.get("/pages/")
    context["top_pages"] = response_data.get("items", [])

    return HttpResponse(template.render(context, request))


def cookies(request):
    template = loader.get_template("main/cookies.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))
