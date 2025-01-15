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


""" record details with id passed through
def catalogue_item(request, id):
    template = loader.get_template("search/catalogue/item.html")
    context = {"id": id}
    return HttpResponse(template.render(context, request))
"""


def catalogue_item(request):
    template = loader.get_template("search/catalogue/item.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue_no(request):
    template = loader.get_template("search/catalogue/item-no.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue_other(request):
    template = loader.get_template("search/catalogue/item-other.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue_long(request):
    template = loader.get_template("search/catalogue/item-long.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))


def catalogue_item_digitised(request):
    template = loader.get_template("search/catalogue/item-digitised.html")
    context = {"foo": "bar"}
    return HttpResponse(template.render(context, request))
