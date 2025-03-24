from typing import Any, Dict, List, Optional

from app.lib.api import JSONAPIClient
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests.exceptions import ConnectionError, RequestException


def delivery_options_request_handler(iaid: str) -> List[Dict[str, Any]]:
    """
    Makes an API call to the delivery options service to fetch available
    delivery options for a given iaid.

    Args:
        iaid (str): The item archive ID to retrieve delivery options for

    Returns:
        List[Dict[str, Any]]: The delivery options data for the specified item

    Raises:
        ImproperlyConfigured: If the DELIVERY_OPTIONS_API_URL setting is not configured
        ValueError: If the API request fails or returns invalid data
    """
    # Validate API URL configuration
    api_url = getattr(settings, "DELIVERY_OPTIONS_API_URL", "").strip()

    if api_url == "":
        raise ImproperlyConfigured("DELIVERY_OPTIONS_API_URL not set")

    try:
        # Create API client
        client = JSONAPIClient(api_url)
        client.add_parameters({"iaid": iaid})

        # Attempt to get data with specific error handling
        try:
            data = client.get()
        except ConnectionError as e:
            raise ValueError(
                f"Failed to retrieve delivery options: Connection error - {str(e)}"
            )
        except RequestException as e:
            raise ValueError(
                f"Failed to retrieve delivery options: Request error - {str(e)}"
            )

        # Validate response structure
        if not data or not isinstance(data, list):
            raise ValueError(
                "Invalid API response format: expected a non-empty list"
            )

        # Ensure each item in the list has the required keys
        for item in data:
            if not all(key in item for key in ["options", "surrogateLinks"]):
                raise ValueError("Invalid API response: missing required keys")

        return data

    except Exception as e:
        # Log the original exception for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Delivery options request error: {str(e)}")

        # Re-raise with a more informative message
        raise
