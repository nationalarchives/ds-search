from typing import Optional

from app.lib.api import JSONAPIClient
from django.conf import settings


def get_delivery_option(iaid: Optional[str] = None):
    api_url = settings.DELIVERY_OPTIONS_CLIENT_BASE_URL

    if not api_url:
        raise Exception("DELIVERY_OPTIONS_CLIENT_BASE_URL not set")

    client = JSONAPIClient(api_url)
    client.add_parameters({"iaid": iaid})

    data = client.get()
    return data
