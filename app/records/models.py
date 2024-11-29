from __future__ import annotations

import re
from typing import Any, Dict, Optional

from app.ciim.models import APIModel
from app.ciim.utils import NOT_PROVIDED, ValueExtractionError, extract
from django.utils.functional import cached_property

from .converters import IDConverter


class Record(APIModel):
    """A 'lazy' data-interaction layer for record data retrieved from the Client API"""

    def __init__(self, raw_data: Dict[str, Any]):
        """
        This method recieves the raw JSON data dict recieved from
        Client API and makes it available to the instance as `self._raw`.
        """
        self._raw = raw_data.get("detail") or raw_data

    @classmethod
    def from_api_response(cls, response: dict) -> Record:
        return cls(response)

    def __str__(self):
        return f"{self.iaid}"

    def get(self, key: str, default: Optional[Any] = NOT_PROVIDED) -> Any:
        """
        Attempts to extract `key` from `self._raw` and return the value.

        Raises `ciim.utils.ValueExtractionError` if the value cannot be extracted.
        """
        if "." in key:
            return extract(self._raw, key, default)
        try:
            return self._raw[key]
        except KeyError as e:
            if default is NOT_PROVIDED:
                raise ValueExtractionError(str(e))
            return default

    @cached_property
    def template(self) -> Dict[str, Any]:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details", default={})

    @cached_property
    def iaid(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        iaid = self.template.get("iaid", "")

        if re.match(IDConverter.regex, iaid):
            # value is not guaranteed to be a valid 'iaid', so we must
            # check it before returning it as one
            return iaid
        return ""
