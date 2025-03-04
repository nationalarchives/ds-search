import base64
import json
import re
from datetime import datetime
from urllib.parse import urlencode

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def base64_encode(s):
    s = bytes(s, "utf-8")
    s = base64.b64encode(s)
    return s.decode("utf-8", "ignore")


def base64_decode(s):
    s = base64.b64decode(s)
    return s.decode("utf-8", "ignore")


def now_iso_8601():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return now_date


def dump_json(obj):
    return json.dumps(obj, indent=2)


def format_number(num):
    return format(num, ",")


def qs_is_value_active(existing_qs, filter, by):
    """Active when identical key/value in existing query string."""
    qs_set = {(filter, str(by))}
    # Not active if either are empty.
    if not existing_qs or not qs_set:
        return False
    # See if the intersection of sets is the same.
    existing_qs_set = set(existing_qs.items())
    return existing_qs_set.intersection(qs_set) == qs_set


def qs_toggle_value(existing_qs, filter, by):
    """Resolve filter against an existing query string."""
    qs = {filter: by}
    # Don't change the currently rendering existing query string!
    rtn_qs = existing_qs.copy()
    # Test for identical key and value in existing query string.
    if qs_is_value_active(existing_qs, filter, by):
        # Remove so that buttons toggle their own value on and off.
        rtn_qs.pop(filter)
    else:
        # Update or add the query string.
        rtn_qs.update(qs)
    return urlencode(rtn_qs)


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
            "qs_is_value_active": qs_is_value_active,
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
        }
    )
    return env
