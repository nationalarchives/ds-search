from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from django.urls import NoReverseMatch, reverse
from django.utils.functional import cached_property
from pyquery import PyQuery as pq

from .converters import IDConverter

logger = logging.getLogger(__name__)


class APIModel(ABC):
    """Model representation of API data.."""

    @classmethod
    @abstractmethod
    def from_api_response(cls, response: dict) -> APIModel:
        """Transform a response From Client API into an APIModel instance.

        To be implemented the concrete class.
        """
        raise NotImplementedError

    @classmethod
    def format_link(self, link_html: str, inc_msg: str = "") -> Dict[str, str]:
        """
        Extracts iaid and text from a link HTML string, e.g. "<a href="C5789">DEFE 31</a>"
        and returns as dict in the format: `{"id":"C5789", "href": "/catalogue/id/C5789/", "text":"DEFE 31"}

        inc_msg includes message with logger if sepcified
        Ex:inc_msg <method_name>:Record(<id):"
        """
        document = pq(link_html)
        iaid = document.attr("href")
        try:
            href = reverse(
                "details-page-machine-readable", kwargs={"iaid": iaid}
            )
        except NoReverseMatch:
            href = ""
            # warning for partially valid data
            logger.warning(
                f"{inc_msg}format_link:No reverse match for details-page-machine-readable with iaid={iaid}"
            )
        return {"id": iaid or "", "href": href, "text": document.text()}


class ValueExtractionError(Exception):
    pass


def extract(
    source: Dict[str, Any], key: str, default: Optional[Any] = None
) -> Any:
    """
    Attempts to extract `key` (a string with multiple '.' to indicate
    traversal) from `source` (a complex multi-level dict where values may
    by lists or other complex types) and return the value.

    If `default` is provided, that value will be returned if any issues
    arise during the process. When no `default` is provied, a
    `ValueExtractionError` is raised instead.
    """
    current = source
    lookups = tuple(key.split("."))

    try:
        for bit in lookups:
            # NOTE: we could use a series of nested try/excepts here instead,
            # but using conditionals allows us to raise more relevant exceptions

            # Only attempt key lookups for dicts
            if isinstance(current, dict):
                current = current[bit]
                continue

            # Only attempt index lookups for sequences, and only
            # when the value looks like an index
            if hasattr(current, "__getitem__"):
                try:
                    bit_index = int(bit)
                except ValueError:
                    pass
                else:
                    current = current[bit_index]  # do index lookup
                    continue

            # Always fall back to attribute lookup
            current = getattr(current, bit)

    except Exception:
        return default

    return current


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

    def get(self, key: str, default: Optional[Any] = "") -> Any:
        """
        Attempts to extract `key` from `self._raw` and return the value.
        """
        if "." in key:
            try:
                return extract(self._raw, key, default)
            except ValueExtractionError:
                return default or ""
        try:
            return self._raw[key]
        except KeyError:
            return default or ""

    @cached_property
    def iaid(self) -> str:
        """
        Return the "iaid" value for this record. If the data is unavailable,
        or is not a valid iaid, a blank string is returned.
        """
        try:
            candidate = self.get("@template.details.iaid")
        except KeyError:
            candidate = ""

        # value from other places
        identifiers = self.get("@template.details.identifier", ())
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
        return self.get("@template.details.source", "")

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
        if candidate := self.get("@template.details.referenceNumber", ""):
            return candidate

        # value from other places
        identifiers = self.get("@template.details.identifier", [])
        for item in identifiers:
            try:
                return item["reference_number"]
            except KeyError:
                pass

        return ""

    @cached_property
    def title(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.title", "")

    @cached_property
    def summary_title(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        if details_summary_title := self.get("@template.details.summaryTitle"):
            return details_summary_title
        return self.get("@template.details.summary.title", "")

    @cached_property
    def date_covering(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.dateCovering", "")

    @cached_property
    def creator(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.get("@template.details.creator", [])

    @cached_property
    def dimensions(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.dimensions", "")

    @cached_property
    def former_department_reference(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.formerDepartmentReference", "")

    @cached_property
    def former_pro_reference(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.formerProReference", "")

    @cached_property
    def language(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.language", "")

    @cached_property
    def legal_status(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.legalStatus", "")

    @cached_property
    def level(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.level.value", "")

    @cached_property
    def level_code(self) -> int | None:
        """Returns the api value of the attr if found, None otherwise."""
        if details_level_code := self.get("@template.details.level.code"):
            return details_level_code
        return self.get("@template.details.level.code", "")

    @cached_property
    def map_designation(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.mapDesignation", "")

    @cached_property
    def map_scale(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.mapScale", "")

    @cached_property
    def note(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.note", "")

    @cached_property
    def physical_condition(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.physicalCondition", "")

    @cached_property
    def physical_description(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.physicalDescription", "")

    @cached_property
    def held_by(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.heldBy", "")

    @cached_property
    def held_by_id(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.heldById", "")

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
        return self.get("@template.details.accessCondition", "")

    @cached_property
    def closure_status(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.closureStatus", "")

    @cached_property
    def record_opening(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.recordOpening", "")

    @cached_property
    def accruals(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.accruals", "")

    @cached_property
    def accumulation_dates(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.accumulationDates", "")

    @cached_property
    def appraisal_information(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.appraisalInformation", "")

    @cached_property
    def copies_information(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.copiesInformation", "")

    @cached_property
    def custodial_history(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.custodialHistory", "")

    @cached_property
    def immediate_source_of_acquisition(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.get("@template.details.immediateSourceOfAcquisition", [])

    @cached_property
    def location_of_originals(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.get("@template.details.locationOfOriginals", [])

    @cached_property
    def restrictions_on_use(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.restrictionsOnUse", "")

    @cached_property
    def administrative_background(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.administrativeBackground", "")

    @cached_property
    def arrangement(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.arrangement", "")

    @cached_property
    def publication_note(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.get("@template.details.publicationNote", [])

    @cached_property
    def related_materials(self) -> tuple[dict[str, Any], ...]:
        """Returns transformed data which is a tuple of dict if found, empty tuple otherwise."""
        inc_msg = f"related_materials:Record({self.iaid}):"
        return tuple(
            dict(
                description=item.get("description", ""),
                links=list(
                    self.format_link(val, inc_msg)
                    for val in item.get("links", ())
                ),
            )
            for item in self.get("@template.details.relatedMaterials", ())
        )

    @cached_property
    def description(self) -> str:
        """Returns the api value of the attr if found, empty str otherwise."""
        return self.get("@template.details.description", "")

    @cached_property
    def separated_materials(self) -> tuple[dict[str, Any], ...]:
        """Returns transformed data which is a tuple of dict if found, empty tuple otherwise."""
        inc_msg = f"separated_materials:Record({self.iaid}):"
        return tuple(
            dict(
                description=item.get("description", ""),
                links=list(
                    self.format_link(val, inc_msg)
                    for val in item.get("links", ())
                ),
            )
            for item in self.get("@template.details.separatedMaterials", ())
        )

    @cached_property
    def unpublished_finding_aids(self) -> list[str]:
        """Returns the api value of the attr if found, empty list otherwise."""
        return self.get("@template.details.unpublishedFindingAids", [])

    @cached_property
    def hierarchy(self) -> tuple[Record, ...]:
        """Returns tuple of records transformed from the values of the attr if found, empty tuple otherwise."""
        return tuple(
            Record({"@template": {"details": item}})
            for item in self.get("@template.details.@hierarchy", ())
            if item.get("identifier")
        )

    @cached_property
    def next(self) -> Record | None:
        """Returns a record transformed from the values of the attr if found, None otherwise."""
        if next := self.get("@template.details.@next", None):
            return Record({"@template": {"details": next}})

    @cached_property
    def previous(self) -> Record | None:
        """Returns a record transformed from the values of the attr if found, None otherwise."""
        if previous := self.get("@template.details.@previous", None):
            return Record({"@template": {"details": previous}})

    @cached_property
    def parent(self) -> Record | None:
        """Returns a record transformed from the values of the attr if found, None otherwise."""
        if parent := self.get("@template.details.parent", None):
            return Record({"@template": {"details": parent}})

    @cached_property
    def is_tna(self) -> bool:
        """Returns True if record belongs to TNA, False otherwise."""
        for item in self.get("@template.details.groupArray", []):
            if item.get("value", "") == "tna":
                return True
        return False

    @cached_property
    def is_digitised(self) -> bool:
        """Returns True if digitised, False otherwise."""
        return self.get("@template.details.digitised", False)
