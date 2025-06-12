from http import HTTPStatus

from django.shortcuts import render


def page_not_found_error_view(request, exception=None):
    response = render(request, "errors/page_not_found.html")
    response.status_code = HTTPStatus.NOT_FOUND
    return response


def server_error_view(request, exception=None):
    response = render(request, "errors/server_error.html")
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response
