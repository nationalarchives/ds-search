from ipaddress import ip_address
import json
import logging
import re
from typing import Any, Dict, List, Optional, Union

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest

from app.deliveryoptions.constants import (
    IP_ONSITE_RANGES,
    IP_STAFFIN_RANGES,
    DCS_PREFIXES,
    AvailabilityCondition,
    delivery_option_tags,
)
from app.deliveryoptions.departments import DEPARTMENT_DETAILS
from app.deliveryoptions.helpers import get_dept
from app.deliveryoptions.reader_type import get_reader_type
from app.records.models import Record

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
        The parsed delivery options configuration
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


def has_distressing_content_match(reference: str) -> bool:
    """
    Check if a reference number matches any of the distressing content prefixes.

    Args:
        reference: The reference number to check

    Returns:
        True if the reference number starts with any distressing content prefix
    """

    return list(filter(reference.startswith, DCS_PREFIXES)) != []


def get_delivery_option_dict(cache: Dict, record_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a record from the cache by its ID.

    Args:
        cache: The cache dictionary
        record_id: The record ID to retrieve

    Returns:
        The record if found, None otherwise
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
        The string with placeholders replaced with actual values

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
        The processed HTML content
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


def surrogate_link_builder(surrogates: List) -> List[Any]:
    """
    Extract surrogate links and AV media links from surrogate data.

    Args:
        surrogates: The list of surrogate data

    Returns:
        A list containing surrogate links (including AV media links)
    """
    surrogate_list = []

    for s in surrogates:
        if s["xReferenceURL"]:
            surrogate_list.append(s["xReferenceURL"])

    return surrogate_list


def generic_builder(
    delivery_option_data: Union[List, str],
    record_data: Record,
    api_surrogate_data: List = None,
    builder_type: str = 'default'
) -> Union[str, List]:
    """
    A generic builder function to handle various delivery option content types.

    Args:
        delivery_option_data: The data to process
        record_data: The record object
        api_surrogate_data: List of surrogate data
        builder_type: Type of builder to determine special processing

    Returns:
        Processed content (str or List) based on the builder type
    """
    # Handle special case for distressing content
    dcs_flag = False
    if builder_type == 'description' and has_distressing_content_match(record_data.reference_number):
        dcs_flag = True

    # Default HTML building
    if builder_type == 'orderbuttons' and isinstance(delivery_option_data, list):
        result = []
        for item in delivery_option_data:
            processed_item = {}
            for key, value in item.items():
                if key in ['href', 'text']:
                    processed_item[key] = html_builder(
                        value, 
                        record_data, 
                        api_surrogate_data=api_surrogate_data
                    )
                else:
                    processed_item[key] = value
            result.append(processed_item)
        return result

    # Standard HTML building
    return html_builder(
        delivery_option_data, 
        record_data, 
        api_surrogate_data=api_surrogate_data, 
        dcs=dcs_flag
    )

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
        The constructed delivery options
    """

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
    delivery_option = get_delivery_option_dict(do_dict, api_result[0]["options"])

    reader_option = delivery_option["readertype"][reader_type]

    # Mapping of builder types for different option keys
    builder_mappings = {
        'heading': ('do_heading', 'heading'),
        'description': ('do_description', 'description'),
        'supplementalcontent': ('do_supplemental', 'supplemental'),
        'orderbuttons': ('do_orderbuttons', 'orderbuttons'),
        'expandlink': ('do_expandlink', 'expandlink'),
        'basketlimit': ('do_basketlimit', 'basketlimit')
    }

    for option_key, (context_key, builder_type) in builder_mappings.items():
        if content := reader_option.get(option_key):
            delivery_options_context_dict[context_key] = generic_builder(
                content, 
                record, 
                api_surrogate_data=do_surrogate, 
                builder_type=builder_type
            )

    return delivery_options_context_dict

