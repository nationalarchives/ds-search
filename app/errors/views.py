from django.shortcuts import render


def custom_404_error_view(request, exception=None):
    response = render(request, "404.html")
    response.status_code = 404
    return response
