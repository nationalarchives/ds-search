import json
import logging
import re
from ipaddress import ip_address
from typing import Any, Dict, List, Optional, Union

from app.deliveryoptions.constants import (
    IP_ONSITE_RANGES,
    IP_STAFFIN_RANGES,
    AvailabilityCondition,
    delivery_option_tags,
)
from app.deliveryoptions.departments import DEPARTMENT_DETAILS
from app.deliveryoptions.helpers import get_dept
from app.deliveryoptions.reader_type import get_reader_type
from app.lib.utils import validate_setting
from app.records.models import Record
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest

logger = logging.getLogger(__name__)

# Dictionary to serve as a cache for file contents, preventing redundant file reads
file_cache = {}


def read_delivery_options(file_path: str) -> Dict:
    """
    Read and parse the delivery options JSON configuration file.

    Uses a file cache to avoid re-reading the same file multiple times.

    Args:
        file_path: Path to the delivery options JSON file

    Returns:
        Dict: The parsed delivery options configuration
    """
    # Check if file content is already in the cache
    if file_path not in file_cache:
        # Open the file in read mode
        with open(file_path, "r") as file:
            # Load the JSON content from the file
            file_content = json.load(file)

            # Cache the file content for future use
            file_cache[file_path] = file_content

    # Return the file content either from the cache or newly loaded
    return file_cache[file_path]


def get_dcs_prefixes() -> List[str]:
    """
    Get the list of prefixes for records with distressing content.

    Returns:
        List[str]: The list of prefixes for records with distressing content
    """
    # Define a cache key
    cache_key = "dcs_prefixes"

    # Try to get the result from the cache
    cached_prefixes = cache.get(cache_key)
    if cached_prefixes is not None:
        return cached_prefixes

    # If not in cache, compute the prefixes
    dcs = validate_setting(
        settings, "DELIVERY_OPTIONS_DCS_LIST", str, default=""
    )

    prefixes = []
    if (
        dcs
    ):  # This check is sufficient since validate_setting ensures dcs is a string or default
        prefixes = [prefix.strip() for prefix in dcs.split(",")]
    else:
        logger.error("Malformed or missing DCS string")

    # Store the result in the cache
    cache.set(cache_key, prefixes, 60 * 60 * 24)  # Cache for 24 hours
    return prefixes


def has_distressing_content_match(reference: str) -> bool:
    """
    Check if a reference number matches any of the distressing content prefixes.

    Args:
        reference: The reference number to check

    Returns:
        bool: True if the reference number starts with any distressing content prefix
    """
    dcs_prefixes = get_dcs_prefixes()

    return list(filter(reference.startswith, dcs_prefixes)) != []


def get_record(cache: Dict, record_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a record from the cache by its ID.

    Args:
        cache: The cache dictionary
        record_id: The record ID to retrieve

    Returns:
        Optional[Dict[str, Any]]: The record if found, None otherwise
    """
    try:
        return cache["deliveryOptions"]["option"][record_id]
    except Exception:
        return None


def html_replacer(value: str, record: Record, api_surrogate_data: List) -> str:
    """
    Replace placeholders in a string with actual values.

    Finds all tags in the format {TagName} and replaces them with
    the result of calling the corresponding function from delivery_option_tags.

    Args:
        value: The string containing placeholders
        record: The record object
        api_surrogate_data: List of surrogate data

    Returns:
        str: The string with placeholders replaced with actual values

    Raises:
        Exception: If a placeholder function call fails
    """
    subs = re.findall(r"{[A-Za-z]*}", value)

    for s in subs:
        try:
            func = delivery_option_tags[s]

            # If the tag doesn't have any data (can happen with surrogate links),
            # rather than have a string with something missing, just return an
            # empty string and it won't get displayed
            if f := func(record, api_surrogate_data):
                value = value.replace(s, f)
        except Exception:
            raise
    return value


def html_builder(
    delivery_option_data: Union[List, str],
    record_data: Record,
    api_surrogate_data: List = None,
    dcs: bool = False,
) -> str:
    """
    Build HTML content from delivery option data, replacing placeholders.

    Args:
        delivery_option_data: The delivery option data to process
        record_data: The record object
        api_surrogate_data: List of surrogate data
        dcs: Whether to include distressing content section

    Returns:
        str: The processed HTML content
    """
    html = ""

    # The description can contain an ordinary description and a DCS description. Which one
    # is chosen is down to whether the document reference prefix matches any in
    # DELIVERY_OPTIONS_DCS_LIST. So, if the code finds a descriptionDCS record but
    # the prefix doesn't match, it skips it.

    if isinstance(delivery_option_data, list):
        for item in delivery_option_data:
            if not dcs and item["name"] == "descriptionDCS":
                pass
            else:
                html += html_replacer(
                    item["value"], record_data, api_surrogate_data
                )
    else:
        html = html_replacer(
            delivery_option_data, record_data, api_surrogate_data
        )

    return html


# Specific pre-processing for the order buttons data
def orderbuttons_builder(
    delivery_option_data: List, record_data: Record, api_surrogate_data: List
) -> List:
    """
    Process order buttons data, replacing placeholders.

    Args:
        delivery_option_data: The order buttons data
        record_data: The record object
        api_surrogate_data: List of surrogate data

    Returns:
        List: The processed order buttons data
    """

    result = []

    for item in delivery_option_data:
        # Create a new dictionary with the same content
        processed_item = {}

        # Copy all key/value pairs, processing 'href' and 'text' if present
        for key, value in item.items():
            if key == "href" or key == "text":
                processed_item[key] = html_builder(
                    value, record_data, api_surrogate_data=api_surrogate_data
                )
            else:
                processed_item[key] = value

        result.append(processed_item)

    return result


# Specific pre-processing for the basket limit data
def basketlimit_builder(
    delivery_option_data: Union[List, str], record_data: Record
) -> str:
    """
    Process basket limit data, replacing placeholders.

    Args:
        delivery_option_data: The basket limit data
        record_data: The record object

    Returns:
        str: The processed basket limit HTML
    """
    return html_builder(delivery_option_data, record_data)


# Specific pre-processing for the expand link data
def expandlink_builder(
    delivery_option_data: Union[List, str], record_data: Record
) -> str:
    """
    Process expand link data, replacing placeholders.

    Args:
        delivery_option_data: The expand link data
        record_data: The record object

    Returns:
        str: The processed expand link HTML
    """
    return html_builder(delivery_option_data, record_data)


# Specific pre-processing for the description data
def description_builder(
    delivery_option_data: Union[List, str],
    record_data: Record,
    api_surrogate_data: List,
) -> str:
    """
    Process description data, replacing placeholders.

    Handles special case for distressing content.

    Args:
        delivery_option_data: The description data
        record_data: The record object
        api_surrogate_data: List of surrogate data

    Returns:
        str: The processed description HTML
    """
    if has_distressing_content_match(record_data.reference_number):
        return html_builder(
            delivery_option_data,
            record_data,
            api_surrogate_data=api_surrogate_data,
            dcs=True,
        )

    return html_builder(
        delivery_option_data, record_data, api_surrogate_data=api_surrogate_data
    )


# Specific pre-processing for the supplemental data
def supplemental_builder(
    delivery_option_data: Union[List, str],
    record_data: Record,
    api_surrogate_data: List,
) -> str:
    """
    Process supplemental data, replacing placeholders.

    Args:
        delivery_option_data: The supplemental data
        record_data: The record object
        api_surrogate_data: List of surrogate data

    Returns:
        str: The processed supplemental HTML
    """
    return html_builder(
        delivery_option_data, record_data, api_surrogate_data=api_surrogate_data
    )


# Specific pre-processing for the heading
def heading_builder(
    delivery_option_data: str, record_data: Record, api_surrogate_data: List
) -> str:
    """
    Process heading data, replacing placeholders.

    Args:
        delivery_option_data: The heading data
        record_data: The record object
        api_surrogate_data: List of surrogate data

    Returns:
        str: The processed heading HTML
    """
    return html_builder(
        delivery_option_data, record_data, api_surrogate_data=api_surrogate_data
    )


def surrogate_link_builder(surrogates: List) -> List[Any]:
    """
    Extract surrogate links and AV media links from surrogate data.

    Args:
        surrogates: The list of surrogate data

    Returns:
        List[Any]: A list containing surrogate links (including AV media links)
    """
    surrogate_list = []

    for s in surrogates:
        if s["xReferenceURL"]:
            surrogate_list.append(s["xReferenceURL"])

    return surrogate_list


def construct_delivery_options(
    api_result: List, record: Record, request: HttpRequest
) -> Dict[str, Any]:
    """
    Construct delivery options based on record and request information.

    This is the main function called from records.py to build the delivery options
    for a record.

    Args:
        api_result: List of delivery options
        record: The record object
        request: The HTTP request

    Returns:
        Dict[str, Any]: The constructed delivery options
    """
    # To do: The api_result list contains zero or more dictionaries. Only 1 should be
    # allowed, so fail on zero or greater than 1

    if api_length := len(api_result) > 1:
        raise ValueError(
            f"Too many results ({api_length}) from DORIS database for IAID {record.iaid}"
        )

    delivery_options_context_dict = {}

    reader_type = get_reader_type(request)

    delivery_options_context_dict["reader_type"] = reader_type

    do_dict = read_delivery_options(settings.DELIVERY_OPTIONS_CONFIG)

    # Surrogate links is always present as a list, which can be empty
    do_surrogate = surrogate_link_builder(api_result[0]["surrogateLinks"])

    if (
        api_result[0]["options"]
        == AvailabilityCondition.ClosedRetainedDeptKnown
    ):
        # Special case. Sometimes, for record type 14 (ClosedRetainedDeptKnown), the department name does not match
        # any entry in the DEPARTMENT_DETAILS dictionary. This shouldn't happen but it does. Therefore, reset the type
        # with that for AvailabilityCondition.ClosedRetainedDeptUnKnown
        if not get_dept(record.reference_number, "deptname"):
            api_result[0][
                "options"
            ] = AvailabilityCondition.ClosedRetainedDeptUnKnown

    # Get the specific delivery option for this artefact
    delivery_option = get_record(do_dict, api_result[0]["options"])

    reader_option = delivery_option["readertype"][reader_type]

    if heading := reader_option.get("heading"):
        delivery_options_context_dict["do_heading"] = heading_builder(
            heading, record, do_surrogate
        )

    if text := reader_option.get("description"):
        delivery_options_context_dict["do_description"] = description_builder(
            text, record, do_surrogate
        )

    if supp := reader_option.get("supplementalcontent"):
        delivery_options_context_dict["do_supplemental"] = supplemental_builder(
            supp, record, do_surrogate
        )

    if obutton := reader_option.get("orderbuttons"):
        delivery_options_context_dict["do_orderbuttons"] = orderbuttons_builder(
            obutton, record, do_surrogate
        )

    if expand := reader_option.get("expandlink"):
        delivery_options_context_dict["do_expandlink"] = expandlink_builder(
            expand, record
        )

    if basket := reader_option.get("basketlimit"):
        delivery_options_context_dict["do_basketlimit"] = basketlimit_builder(
            basket, record
        )

    return delivery_options_context_dict
