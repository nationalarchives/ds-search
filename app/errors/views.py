import logging
from http import HTTPStatus

from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import TemplateDoesNotExist, TemplateSyntaxError

logger = logging.getLogger(__name__)


def page_not_found_error_view(request, exception=None):
    try:
        response = render(request, "errors/page_not_found.html")
    except TemplateDoesNotExist as e:
        logger.error(f"Template missing: {e}")
        return HttpResponseServerError(
            "Internal Server Error: Template not found."
        )
    response.status_code = HTTPStatus.NOT_FOUND
    return response


def server_error_view(request, exception=None):
    try:
        response = render(request, "errors/server_error.html")
    except TemplateDoesNotExist as e:
        logger.error(f"Template missing: {e}")
        return HttpResponseServerError(
            "Internal Server Error: Template not found."
        )
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response
