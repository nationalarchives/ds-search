import logging
from typing import Any, Dict

from django.urls import NoReverseMatch, reverse
from pyquery import PyQuery as pq

logger = logging.getLogger(__name__)


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
        href = reverse("details-page-machine-readable", kwargs={"id": iaid})
    except NoReverseMatch:
        href = ""
        # warning for partially valid data
        logger.warning(
            f"{inc_msg}format_link:No reverse match for details-page-machine-readable with iaid={iaid}"
        )
    return {"id": iaid or "", "href": href, "text": document.text()}


def extract(source: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Attempts to extract `key` (a string with multiple '.' to indicate
    traversal) from `source` (a complex multi-level dict where values may
    by lists or other complex types) and return the value.

    If `default` is provided, that value will be returned if any issues
    arise during the process.
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
