from typing import Any, Dict, Optional

from app.lib.api import JSONAPIClient
from django.conf import settings


def get_delivery_option(iaid: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve delivery options data for a specified archive item.

    Makes an API call to the delivery options service to fetch available
    delivery options for a given item.

    Args:
        iaid (Optional[str]): The item archive ID to retrieve delivery options for

    Returns:
        Dict[str, Any]: The delivery options data for the specified item

    Raises:
        Exception: If the DELIVERY_OPTIONS_API_URL setting is not configured
    """
    api_url = settings.DELIVERY_OPTIONS_API_URL

    if not api_url:
        raise Exception("DELIVERY_OPTIONS_API_URL  not set")

    client = JSONAPIClient(api_url)
    client.add_parameters({"iaid": iaid})

    data = client.get()
    return data
