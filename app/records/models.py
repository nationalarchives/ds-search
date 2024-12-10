from __future__ import annotations

import re
from typing import Any, Dict, Optional

from app.ciim.models import APIModel
from app.ciim.utils import NOT_PROVIDED, ValueExtractionError, extract
from django.urls import NoReverseMatch, reverse
from django.utils.functional import cached_property

from .converters import IDConverter


class Record(APIModel):
    """A 'lazy' data-interaction layer for record data retrieved from the Client API"""

    def __init__(self, raw_data: dict[str, Any]):
        """
        This method recieves the raw JSON data dict recieved from
        Client API and makes it available to the instance as `self._raw`.
        """
        self._raw = raw_data

    @classmethod
    def from_api_response(cls, response: dict) -> Record:
        return cls(response)

    def __str__(self):
        return f"{self.summary_title} ({self.iaid})"

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
    def template(self) -> dict[str, Any]:
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

    @cached_property
    def source(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("source", "")

    @cached_property
    def reference_number(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("referenceNumber", "")

    @cached_property
    def title(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("title", "")

    @cached_property
    def summary_title(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("summaryTitle", "")

    @cached_property
    def date_created(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("dateCreated", "")

    @cached_property
    def custom_record_type(self) -> str:
        """
        Returns a custom record type.
        TODO: custom record type for identifying CREATORS.
        """
        return self.source

    @cached_property
    def date_covering(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("dateCovering", "")

    @cached_property
    def creator(self) -> list[str]:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("creator", [])

    @cached_property
    def dimensions(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("dimensions", "")

    @cached_property
    def former_department_reference(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("formerDepartmentReference", "")

    @cached_property
    def former_pro_reference(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("formerProReference", "")

    @cached_property
    def language(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("language", "")

    @cached_property
    def legal_status(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("legalStatus", "")

    @cached_property
    def level(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.level.value", "")

    @cached_property
    def level_code(self) -> int | None:
        """Returns the api value of the attr if found, None otherwise."""
        return self.get("@template.details.level.code", None)

    @cached_property
    def map_designation(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("mapDesignation", "")

    @cached_property
    def map_scale(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("mapScale", "")

    @cached_property
    def note(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("note", "")

    @cached_property
    def physical_condition(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("physicalCondition", "")

    @cached_property
    def physical_description(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("physicalDescription", "")

    @cached_property
    def held_by(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("heldBy", "")

    @cached_property
    def held_by_id(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("heldById", "")

    @cached_property
    def held_by_url(self) -> str:
        """Returns url path if the id is found, empty str otherwise."""
        if self.held_by_id:
            try:
                return reverse(
                    "details-page-machine-readable",
                    kwargs={"id": self.held_by_id},
                )
            except NoReverseMatch:
                pass
        return ""

    @cached_property
    def access_condition(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("accessCondition", "")
