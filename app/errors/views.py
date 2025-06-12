import logging
from http import HTTPStatus

from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import TemplateDoesNotExist, TemplateSyntaxError

logger = logging.getLogger(__name__)

PAGE_NOT_FOUND_TEMPLATE = "errors/page_not_found.html"
SERVER_ERROR_TEMPLATE = "errors/server_error.html"


def page_not_found_error_view(request, exception=None):
    try:
        response = render(request, PAGE_NOT_FOUND_TEMPLATE)
    except TemplateDoesNotExist as e:
        logger.error(f"Template missing: {e}")
        return HttpResponseServerError(
            "Internal Server Error: Template not found."
        )
    response.status_code = HTTPStatus.NOT_FOUND
    return response


def server_error_view(request, exception=None):
    try:
        response = render(request, SERVER_ERROR_TEMPLATE)
    except TemplateDoesNotExist as e:
        logger.error(f"Template missing: {e}")
        return HttpResponseServerError(
            "Internal Server Error: Template not found."
        )
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response
