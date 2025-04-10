from django.http import HttpResponse
from django.template import loader
from app.lib.api import JSONAPIClient
from django.conf import settings

def index(request):
    template = loader.get_template("main/index.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue(request):
    template = loader.get_template("main/catalogue.html")
    context = {}

    client = JSONAPIClient(settings.ETNA_API_URL)
    client.add_parameters({"child_of": 55, "limit": 3, "order": "-first_published_at"})
    response_data = client.get("/pages/")
    context['pages'] = response_data.get("items", [])

    client.add_parameters({"child_of": 5, "limit": 3, "order": "-first_published_at"})
    response_data = client.get("/pages/")
    context['top_pages'] = response_data.get("items", [])

    return HttpResponse(template.render(context, request))


def cookies(request):
    template = loader.get_template("main/cookies.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))
