import json
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, Tuple, Type

import requests
from app.records.models import Record
from django.utils.functional import cached_property

from .exceptions import (
    ClientAPIBadRequestError,
    ClientAPICommunicationError,
    ClientAPIInternalServerError,
    ClientAPIServiceUnavailableError,
    DoesNotExist,
    MultipleObjectsReturned,
)

if TYPE_CHECKING:
    from app.ciim.models import APIModel


class ResultList:
    """
    A convenience class that lazily converts a raw list of "hits" (from various
    API endpoints) into instances of `item_type` when iterated.
    """

    def __init__(
        self,
        hits: Sequence[Dict[str, Any]],
        item_type: Type,
    ):
        self._hits = hits or []
        self.item_type = item_type

    @cached_property
    def hits(self) -> Tuple["APIModel"]:
        """
        Return a tuple of APIModel instances representative of the raw `_hits`
        data. The return value is cached to support reuse without any
        transformation overhead.
        """
        return tuple(
            self.item_type.from_api_response(h) if isinstance(h, dict) else h
            for h in self._hits
        )

    def __iter__(self) -> Iterable["APIModel"]:
        yield from self.hits

    def __len__(self) -> int:
        return len(self._hits)

    def __bool__(self) -> bool:
        return bool(self._hits)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.hits}>"


class ClientAPI:
    """Client used to Fetch and validate data from configured external API."""

    http_error_classes = {
        400: ClientAPIBadRequestError,
        500: ClientAPIInternalServerError,
        503: ClientAPIServiceUnavailableError,
    }
    default_http_error_class = ClientAPICommunicationError

    def __init__(
        self,
        base_url: str,
        api_key: str,
        verify_certificates: bool = True,
        timeout: int = 5,
    ):
        self.base_url: str = base_url
        self.session = requests.Session()
        self.session.headers.update({"apikey": api_key})
        self.session.verify = verify_certificates
        self.timeout = timeout

    def resultlist_from_response(
        self,
        response_data: Dict[str, Any],
        item_type: Type = Record,
    ) -> ResultList:
        try:
            hits = response_data["data"]
        except KeyError:
            hits = []

        return ResultList(
            hits=hits,
            item_type=item_type,
        )

    def get(
        self,
        *,
        id: Optional[str] = None,
    ) -> Record:
        """Make request and return response for Client API's /get endpoint.
        Used to get a single item by its identifier.

        Keyword arguments:

        id:
            Generic identifier. Matches various id's
            Ex: returns match on Information Asset Identifier - iaid (or similar primary identifier)
        """
        params = {
            "id": id,
        }

        # Get HTTP response from the API
        response = self.make_request(f"{self.base_url}/get", params=params)

        # Convert the HTTP response to a Python dict
        response_data = response.json()

        # Convert the Python dict to a ResultList
        result_list = self.resultlist_from_response(response_data)

        if not result_list:
            raise DoesNotExist(f"Id {id} does not exist")
        if len(result_list) > 1:
            raise MultipleObjectsReturned(
                f"Multiple records returned for Id {id}"
            )
        return result_list.hits[0]

    def prepare_request_params(
        self, data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Process parameters before passing to Client API.

        Remove empty values to make logged requests cleaner.
        """
        if not data:
            return {}

        return {k: v for k, v in data.items() if v is not None}

    def make_request(
        self, url: str, params: Optional[dict[str, Any]] = None
    ) -> requests.Response:
        """Make request to Client API."""
        params = self.prepare_request_params(params)
        response = self.session.get(url, params=params, timeout=self.timeout)
        self._raise_for_status(response)
        return response

    def _raise_for_status(self, response: requests.Response) -> None:
        """Raise custom error for any requests.HTTPError raised for a request.

        ClientAPIErrors include response body in message to aide debugging.
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_class = self.http_error_classes.get(
                e.response.status_code, self.default_http_error_class
            )

            try:
                response_body = json.dumps(response.json(), indent=4)
            except json.JSONDecodeError:
                response_body = response.text

            raise error_class(
                f"Response body: {response_body}", response=response
            ) from e
