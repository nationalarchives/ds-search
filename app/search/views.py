from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("search/index.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue_index(request):
    template = loader.get_template("search/catalogue/index.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))
