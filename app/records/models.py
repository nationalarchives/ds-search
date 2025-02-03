from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from django.urls import NoReverseMatch, reverse
from django.utils.functional import cached_property
from pydash import objects
from pyquery import PyQuery as pq

from .converters import IDConverter

logger = logging.getLogger(__name__)


NOT_PROVIDED = "__np__"


class APIModel(ABC):
    """Model representation of API data.."""

    @classmethod
    @abstractmethod
    def from_api_response(cls, response: dict) -> APIModel:
        """Transform a response From Client API into an APIModel instance.

        To be implemented the concrete class.
        """
        raise NotImplementedError


def format_link(link_html: str, inc_msg: str = "") -> Dict[str, str]:
    """
    Extracts iaid and text from a link HTML string, e.g. "<a href="C5789">DEFE 31</a>"
    and returns as dict in the format: `{"id":"C5789", "href": "/catalogue/id/C5789/", "text":"DEFE 31"}

    inc_msg includes message with logger if sepcified
    Ex:inc_msg <method_name>:Record(<id):"
    """
    document = pq(link_html)
    iaid = document.attr("href")
    try:
        href = reverse("details-page-machine-readable", kwargs={"iaid": iaid})
    except NoReverseMatch:
        href = ""
        # warning for partially valid data
        logger.warning(
            f"{inc_msg}format_link:No reverse match for details-page-machine-readable with iaid={iaid}"
        )
    return {"id": iaid or "", "href": href, "text": document.text()}


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
        """
        return objects.get(self._raw, key, default)

    @cached_property
    def template(self) -> dict[str, Any]:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details", default={})

    @cached_property
    def iaid(self) -> str:
        """
        Return the "iaid" value for this record. If the data is unavailable,
        or is not a valid iaid, a blank string is returned.
        """
        candidate = self.get("@template.details.iaid", "")

        if not candidate:
            candidate = self.get("@template.details.primaryIdentifier", "")

        if not candidate:
            # value from other places
            if identifiers := self.get("identifier", []):
                for item in identifiers:
                    try:
                        candidate = item["iaid"]
                    except KeyError:
                        candidate = ""

        if candidate and re.match(IDConverter.regex, candidate):
            # value is not guaranteed to be a valid 'iaid', so we must
            # check it before returning it as one
            return candidate
        return ""

    @cached_property
    def source(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("source", "")

    @cached_property
    def custom_record_type(self) -> str:
        """
        Returns a custom record type.
        TODO: custom record type for identifying CREATORS.
        """
        return self.source

    @cached_property
    def reference_number(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        try:
            return self.template["referenceNumber"]
        except KeyError:
            pass

        # value from other places
        identifiers = self.get("identifier", "")
        for item in identifiers:
            try:
                return item["reference_number"]
            except KeyError:
                pass

        return ""

    @cached_property
    def title(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("title", "")

    @cached_property
    def summary_title(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        if details_summary_title := self.get("@template.details.summaryTitle"):
            return details_summary_title
        return self.get("summary.title", "")

    @cached_property
    def date_covering(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("dateCovering", "")

    @cached_property
    def creator(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
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
        if details_level_code := self.get("@template.details.level.code"):
            return details_level_code
        return self.get("level.code", "")

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
                    kwargs={"iaid": self.held_by_id},
                )
            except NoReverseMatch:
                # warning for partially valid record
                logger.warning(
                    f"held_by_url:Record({self.iaid}):No reverse match for details-page-machine-readable with held_by_id={self.held_by_id}"
                )
        return ""

    @cached_property
    def access_condition(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("accessCondition", "")

    @cached_property
    def closure_status(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("closureStatus", "")

    @cached_property
    def record_opening(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("recordOpening", "")

    @cached_property
    def accruals(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("accruals", "")

    @cached_property
    def accumulation_dates(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("accumulationDates", "")

    @cached_property
    def appraisal_information(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("appraisalInformation", "")

    @cached_property
    def copies_information(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("copiesInformation", "")

    @cached_property
    def custodial_history(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("custodialHistory", "")

    @cached_property
    def immediate_source_of_acquisition(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.template.get("immediateSourceOfAcquisition", [])

    @cached_property
    def location_of_originals(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.template.get("locationOfOriginals", [])

    @cached_property
    def restrictions_on_use(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("restrictionsOnUse", "")

    @cached_property
    def administrative_background(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("administrativeBackground", "")

    @cached_property
    def arrangement(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("arrangement", "")

    @cached_property
    def publication_note(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.template.get("publicationNote", [])

    @cached_property
    def related_materials(self) -> tuple[dict[str, Any], ...]:
        """Returns transformed data which is a tuple of dict if found, empty tuple otherwise."""
        inc_msg = f"related_materials:Record({self.iaid}):"
        return tuple(
            dict(
                description=item.get("description", ""),
                links=list(
                    format_link(val, inc_msg) for val in item.get("links", ())
                ),
            )
            for item in self.template.get("relatedMaterials", ())
        )

    @cached_property
    def description(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.template.get("description", "")

    @cached_property
    def separated_materials(self) -> tuple[dict[str, Any], ...]:
        """Returns transformed data which is a tuple of dict if found, empty tuple otherwise."""
        inc_msg = f"separated_materials:Record({self.iaid}):"
        return tuple(
            dict(
                description=item.get("description", ""),
                links=list(
                    format_link(val, inc_msg) for val in item.get("links", ())
                ),
            )
            for item in self.template.get("separatedMaterials", ())
        )

    @cached_property
    def unpublished_finding_aids(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.template.get("unpublishedFindingAids", [])

    @cached_property
    def hierarchy(self) -> tuple[Record, ...]:
        """Returns tuple of records transformed from the values of the attr if found, empty tuple otherwise."""
        return tuple(
            Record(item)
            for item in self.template.get("@hierarchy", ())
            if item.get("identifier")
        )

    @cached_property
    def next(self) -> Record | None:
        """Returns a record transformed from the values of the attr if found, None otherwise."""
        if next := self.template.get("@next", None):
            return Record(next)

    @cached_property
    def previous(self) -> Record | None:
        """Returns a record transformed from the values of the attr if found, None otherwise."""
        if previous := self.template.get("@previous", None):
            return Record(previous)

    @cached_property
    def parent(self) -> Record | None:
        """Returns a record transformed from the values of the attr if found, None otherwise."""
        if parent := self.template.get("parent", None):
            return Record(parent)

    @cached_property
    def is_tna(self) -> bool:
        """Returns True if record belongs to TNA, False otherwise."""
        for item in self.template.get("groupArray", []):
            if item.get("value", "") == "tna":
                return True
        return False

    @cached_property
    def is_digitised(self) -> bool:
        """Returns True if digitised, False otherwise."""
        return self.template.get("digitised", False)
