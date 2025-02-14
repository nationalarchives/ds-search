from django.shortcuts import render


def page_not_found_error_view(request, exception=None):
    response = render(request, "errors/page_not_found.html")
    response.status_code = 404
    return response
