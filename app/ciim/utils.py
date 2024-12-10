from typing import Any, Dict, Optional

from django.urls import NoReverseMatch, reverse
from pyquery import PyQuery as pq


class ValueExtractionError(Exception):
    pass


NOT_PROVIDED = "__np__"


def extract(
    source: Dict[str, Any], key: str, default: Optional[Any] = NOT_PROVIDED
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

    except Exception as e:
        if default is NOT_PROVIDED:
            raise ValueExtractionError(
                f"'{key}' could not be extracted. {type(e)} raised when extracting '{bit}' from {current}."
            )
        return default

    return current


def format_link(link_html: str) -> Dict[str, str]:
    """
    Extracts iaid and text from a link HTML string, e.g. "<a href="C5789">DEFE 31</a>"
    and returns as dict in the format: `{"id":"C5789", "href": "/catalogue/id/C5789/", "text":"DEFE 31"}
    """
    document = pq(link_html)
    id = document.attr("href")
    try:
        href = reverse("details-page-machine-readable", kwargs={"id": id})
    except NoReverseMatch:
        href = ""
    return {"id": id, "href": href, "text": document.text()}
