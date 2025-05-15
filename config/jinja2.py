import base64
import json
import re
from datetime import datetime

from app.lib.xslt_transformations import apply_generic_xsl
from django.conf import settings
from django.http import QueryDict
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def sanitise_record_description(s):
    # Remove whitespace between <p> tags
    s = re.sub(r"(</p>)\s+(<p[ >])", r"\1\2", s).strip()
    return s


def base64_encode(s):
    s = bytes(s, "utf-8")
    s = base64.b64encode(s)
    return s.decode("utf-8", "ignore")


def base64_decode(s):
    try:
        s = base64.b64decode(s)
    except Exception:
        return s
    return s.decode("utf-8", "ignore")


def now_iso_8601():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return now_date


def dump_json(obj):
    return json.dumps(obj, indent=2)


def format_number(num):
    try:
        number = int(num)
    except ValueError:
        return num
    return format(number, ",")


def qs_is_value_active(existing_qs: QueryDict, filter: str, by: str):
    """Active when identical key/value in existing query string."""
    qs_set = {(filter, str(by))}
    # Not active if either are empty.
    if not existing_qs or not qs_set:
        return False
    # Test for identical key and value in existing query string.
    return str(by) in existing_qs.getlist(filter)


def qs_toggle_value(
    existing_qs: QueryDict, filter: str, by: str, return_object: bool = False
):
    """Resolve filter against an existing query string."""
    # Don't change the currently rendering existing query string!
    rtn_qs = existing_qs.copy()
    # Test for identical key and value in existing query string.
    if qs_is_value_active(existing_qs, filter, by):
        # Create a copy of the list.
        new_list = rtn_qs.getlist(filter).copy()
        # Remove the value from the list.
        new_list.remove(str(by))
        # If the list is not empty, update the query string with the new list.
        if len(new_list):
            rtn_qs.setlist(filter, new_list)
        else:
            rtn_qs.pop(filter)
    else:
        # Add the key/value pair to the query string.
        qs = {filter: by}
        # Update the query string with the new key/value pair.
        rtn_qs.update(qs)
    # Return the query string as a QueryDict object or as a URL encoded string.
    return rtn_qs if return_object else rtn_qs.urlencode()


def qs_replace_value(
    existing_qs: QueryDict, filter: str, by: str, return_object: bool = False
):
    # Don't change the currently rendering existing query string!
    rtn_qs = existing_qs.copy()
    rtn_qs[filter] = by
    return rtn_qs if return_object else rtn_qs.urlencode()


def qs_append_value(
    existing_qs: QueryDict, filter: str, by: str, return_object: bool = False
):
    # Don't change the currently rendering existing query string!
    rtn_qs = existing_qs.copy()
    if filter and not qs_is_value_active(existing_qs, filter, by):
        qs = {filter: by}
        rtn_qs.update(qs)
    return rtn_qs if return_object else rtn_qs.urlencode()


def qs_remove_value(
    existing_qs: QueryDict, filter: str, return_object: bool = False
):
    # Don't change the currently rendering existing query string!
    rtn_qs = existing_qs.copy()
    if filter in rtn_qs:
        rtn_qs.pop(filter)
    return rtn_qs if return_object else rtn_qs.urlencode()


def environment(**options):
    env = Environment(**options)

    TNA_FRONTEND_VERSION = ""
    try:
        with open(
            "/app/node_modules/@nationalarchives/frontend/package.json",
        ) as package_json:
            try:
                data = json.load(package_json)
                TNA_FRONTEND_VERSION = data["version"] or ""
            except ValueError:
                pass
    except FileNotFoundError:
        pass

    env.globals.update(
        {
            "static": static,
            "app_config": {
                "GA4_ID": settings.GA4_ID,
                "TNA_FRONTEND_VERSION": TNA_FRONTEND_VERSION,
                "BUILD_VERSION": settings.BUILD_VERSION,
                "COOKIE_DOMAIN": settings.COOKIE_DOMAIN,
            },
            "feature": {"PHASE_BANNER": settings.FEATURE_PHASE_BANNER},
            "url": reverse,
            "now_iso_8601": now_iso_8601,
            "qs_append_value": qs_append_value,
            "qs_is_value_active": qs_is_value_active,
            "qs_remove_value": qs_remove_value,
            "qs_replace_value": qs_replace_value,
            "qs_toggle_value": qs_toggle_value,
        }
    )
    env.filters.update(
        {
            "slugify": slugify,
            "dump_json": dump_json,
            "format_number": format_number,
            "base64_encode": base64_encode,
            "base64_decode": base64_decode,
            "sanitise_record_description": sanitise_record_description,
            "apply_generic_xsl": apply_generic_xsl,
        }
    )
    return env
