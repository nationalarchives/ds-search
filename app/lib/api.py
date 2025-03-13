import logging

from django.conf import settings
from requests import (
    ConnectionError,
    JSONDecodeError,
    Timeout,
    TooManyRedirects,
    codes,
    get,
)

logger = logging.getLogger(__name__)


class ResourceNotFound(Exception):
    pass


class JSONAPIClient:
    api_url = ""
    params = {}

    def __init__(self, api_url, params={}):
        self.api_url = api_url
        self.params = params

    def add_parameter(self, key, value):
        self.params[key] = value

    def add_parameters(self, params):
        self.params = self.params | params

    def get(self, path="/") -> dict:
        """Makes a request to the config API. Returns decoded json,
        otherwise raises error"""
        url = f"{self.api_url}/{path.lstrip('/')}"
        headers = {
            "Cache-Control": "no-cache",
            # "Accept": "application/json",  # TODO: This breaks the API
        }
        try:
            response = get(
                url,
                params=self.params,
                headers=headers,
            )
        except ConnectionError:
            logger.error("JSON API connection error")
            raise Exception("A connection error occured")
        except Timeout:
            logger.error("JSON API timeout")
            raise Exception("The request timed out")
        except TooManyRedirects:
            logger.error("JSON API had too many redirects")
            raise Exception("Too many redirects")
        except Exception as e:
            logger.error(f"Unknown JSON API exception: {e}")
            raise Exception(str(e))
        logger.debug(response.url)
        if response.status_code == codes.ok:
            try:
                return response.json()
            except JSONDecodeError:
                logger.error("JSON API provided non-JSON response")
                raise Exception("Non-JSON response provided")
        if response.status_code == 400:
            logger.error(f"Bad request: {response.url}")
            raise Exception("Bad request")
        if response.status_code == 403:
            logger.warning("Forbidden")
            raise Exception("Forbidden")
        if response.status_code == 404:
            logger.warning("Resource not found")
            raise ResourceNotFound("Resource not found")
        logger.error(f"JSON API responded with {response.status_code}")
        raise Exception("Request failed")


def rosetta_request_handler(uri, params={}) -> dict:
    """Prepares and initiates the api url requested and returns response data"""
    api_url = settings.ROSETTA_API_URL
    if not api_url:
        raise Exception("ROSETTA_API_URL not set")
    client = JSONAPIClient(api_url)
    client.add_parameters(params)
    data = client.get(uri)
    return data


def iiif_request_handler(uri, params={}) -> dict:
    api_url = settings.IIIF_API_URL
    if not api_url:
        raise Exception("IIIF_API_URL not set")
    client = JSONAPIClient(api_url)
    client.add_parameters(params)
    data = client.get(uri)
    return data