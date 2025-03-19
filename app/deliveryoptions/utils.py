import json
import logging
import os
import re
from ipaddress import ip_address
from typing import Any, Dict, List, Optional, Tuple, Union

from app.deliveryoptions.constants import (
    IP_ONSITE_RANGES,
    IP_STAFFIN_RANGES,
    AvailabilityCondition,
    Reader,
    deliveryOptionsTags,
)
from app.deliveryoptions.departments import DEPARTMENT_DETAILS
from app.deliveryoptions.helpers import get_dept
from app.deliveryoptions.reader_type import (
    get_client_ip,
    is_ip_in_cidr,
)
from app.records.models import Record
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest

logger = logging.getLogger(__name__)

# Dictionary to serve as a cache for file contents, preventing redundant file reads
file_cache = {}


def read_delivery_options(file_path: str) -> List:
    """
    Read and parse the delivery options JSON configuration file.

    Uses a file cache to avoid re-reading the same file multiple times.

    Args:
        file_path: Path to the delivery options JSON file

    Returns:
        List: The parsed delivery options configuration
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
    dcs = settings.DELIVERY_OPTIONS_DCS_LIST
    prefixes = dcs.split()

    # Store the result in the cache (you can specify a timeout in seconds as the third parameter)
    # Using a longer timeout since this likely doesn't change often
    cache.set(cache_key, prefixes, 60 * 60 * 24)  # Cache for 24 hours

    return prefixes


def distressing_content_match(reference: str) -> bool:
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


def html_replacer(string: str, record: Record, surrogate_data: List) -> str:
    """
    Replace placeholders in a string with actual values.

    Finds all tags in the format {TagName} and replaces them with
    the result of calling the corresponding function from deliveryOptionsTags.

    Args:
        string: The string containing placeholders
        record: The record object
        surrogate_data: List of surrogate data

    Returns:
        str: The string with placeholders replaced with actual values

    Raises:
        Exception: If a placeholder function call fails
    """
    subs = re.findall(r"{[A-Za-z]*}", string)

    for s in subs:
        try:
            func = deliveryOptionsTags[s]

            # If the tag doesn't have any data (can happen with surrogate links),
            # rather than have a string with something missing, just return an
            # empty string and it won't get displayed
            if f := func(record, surrogate_data):
                string = string.replace(s, f)
        except Exception:
            raise
    return string


def html_builder(
    delivery_option_data: Union[List, str],
    record_data: Record,
    surrogate_data: List = [],
    dcs: bool = False,
) -> str:
    """
    Build HTML content from delivery option data, replacing placeholders.

    Args:
        delivery_option_data: The delivery option data to process
        record_data: The record object
        surrogate_data: List of surrogate data
        dcs: Whether to include distressing content section

    Returns:
        str: The processed HTML content
    """
    html = ""

    if delivery_option_data is None:
        return html

    if isinstance(delivery_option_data, list):
        for item in delivery_option_data:
            if not dcs and item["name"] == "descriptionDCS":
                pass
            else:
                html += html_replacer(
                    item["value"], record_data, surrogate_data
                )
    else:
        html = html_replacer(delivery_option_data, record_data, surrogate_data)

    return html


# Specific pre-processing for the order buttons data
def orderbuttons_builder(
    delivery_option_data: List, record_data: Record, surrogate_data: List
) -> List:
    """
    Process order buttons data, replacing placeholders.

    Args:
        delivery_option_data: The order buttons data
        record_data: The record object
        surrogate_data: List of surrogate data

    Returns:
        List: The processed order buttons data
    """
    for item in delivery_option_data:
        item["href"] = html_builder(
            item["href"], record_data, surrogate_data=surrogate_data
        )
        item["text"] = html_builder(
            item["text"], record_data, surrogate_data=surrogate_data
        )
    return delivery_option_data


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
    surrogate_data: List,
) -> str:
    """
    Process description data, replacing placeholders.

    Handles special case for distressing content.

    Args:
        delivery_option_data: The description data
        record_data: The record object
        surrogate_data: List of surrogate data

    Returns:
        str: The processed description HTML
    """
    if distressing_content_match(record_data.reference_number):
        return html_builder(
            delivery_option_data,
            record_data,
            surrogate_data=surrogate_data,
            dcs=True,
        )

    return html_builder(
        delivery_option_data, record_data, surrogate_data=surrogate_data
    )


# Specific pre-processing for the supplemental data
def supplemental_builder(
    delivery_option_data: Union[List, str],
    record_data: Record,
    surrogate_data: List,
) -> str:
    """
    Process supplemental data, replacing placeholders.

    Args:
        delivery_option_data: The supplemental data
        record_data: The record object
        surrogate_data: List of surrogate data

    Returns:
        str: The processed supplemental HTML
    """
    return html_builder(
        delivery_option_data, record_data, surrogate_data=surrogate_data
    )


# Specific pre-processing for the heading
def heading_builder(
    delivery_option_data: str, record_data: Record, surrogate_data: List
) -> str:
    """
    Process heading data, replacing placeholders.

    Args:
        delivery_option_data: The heading data
        record_data: The record object
        surrogate_data: List of surrogate data

    Returns:
        str: The processed heading HTML
    """
    return html_builder(
        delivery_option_data, record_data, surrogate_data=surrogate_data
    )


def surrogate_link_builder(surrogates: List) -> Tuple[List[Any], List[Any]]:
    """
    Extract surrogate links and AV media links from surrogate data.

    Args:
        surrogates: The list of surrogate data

    Returns:
        Tuple[List[Any], List[Any]]: A tuple containing surrogate links and AV media links
    """
    surrogate_list = []
    av_media_list = []

    for s in surrogates:
        if s["xReferenceURL"]:
            surrogate_list.append(s["xReferenceURL"])

        if s["xReferenceType"] == "AV_MEDIA":
            if s["xReferenceURL"]:
                av_media_list.append(s["xReferenceURL"])

    return surrogate_list, av_media_list


def is_onsite(visitor_ip_address: str) -> bool:
    """
    Check if a visitor's IP address is within the on-site IP ranges.

    Args:
        visitor_ip_address: The visitor's IP address

    Returns:
        bool: True if the visitor is on-site, False otherwise
    """
    return is_ip_in_cidr(visitor_ip_address, IP_ONSITE_RANGES)


def is_subscribed() -> bool:
    """
    Check if the user has a subscription.

    Returns:
        bool: True if the user has a subscription, False otherwise
    """
    # TODO once user management is in place
    return False


def is_staff(visitor_ip_address: str) -> bool:
    """
    Check if a visitor's IP address is within the staff IP ranges.

    Args:
        visitor_ip_address: The visitor's IP address

    Returns:
        bool: True if the visitor is staff, False otherwise
    """
    return is_ip_in_cidr(visitor_ip_address, IP_STAFFIN_RANGES)


def get_dev_reader_type() -> Reader:
    """
    Get the reader type from the environment variable for development/testing.

    Returns:
        Reader: The reader type from the environment variable or UNDEFINED if not set
    """
    override_reader_type = os.getenv("OVERRIDE_READER_TYPE", Reader.UNDEFINED)

    # If environment variable is set, validate it
    if override_reader_type != Reader.UNDEFINED:
        try:
            # Convert the environment variable to an integer
            reader_value = int(override_reader_type)

            # Check if it's a valid Reader enum value
            if reader_value in Reader._value2member_map_:
                return Reader(
                    reader_value
                )  # Return the corresponding Reader enum value

        except Exception as e:
            logger.warning(
                f"Override reader type '{override_reader_type}' cannot be determined - returning UNDEFINED ({type(e)}: {e.args})"
            )

    return Reader.UNDEFINED  # Default to UNDEFINED


def get_reader_type(request: HttpRequest) -> Reader:
    """
    Determine the reader type based on request information.

    Args:
        request: The HTTP request

    Returns:
        Reader: The determined reader type
    """
    reader = Reader.UNDEFINED

    try:
        visitor_ip_address = get_client_ip(request)
    except Exception as e:
        logger.warning(
            f"Cannot determine the users ip address - returning OFFSITE ({type(e)}: {e.args})"
        )
        return Reader.OFFSITE

    # Check if there is an override of reader type - used for testing and demonstrations.
    reader = get_dev_reader_type()

    if reader == Reader.UNDEFINED:
        if is_subscribed():
            reader = Reader.SUBSCRIPTION
        elif is_onsite(visitor_ip_address):
            reader = Reader.ONSITEPUBLIC
        elif is_staff(visitor_ip_address):
            reader = Reader.STAFFIN
        else:
            reader = Reader.OFFSITE

    return reader


# Main routine called from records.py
def construct_delivery_options(
    doptions: List, record: Record, request: HttpRequest
) -> Dict[str, Any]:
    """
    Construct delivery options based on record and request information.

    This is the main function called from records.py to build the delivery options
    for a record.

    Args:
        doptions: List of delivery options
        record: The record object
        request: The HTTP request

    Returns:
        Dict[str, Any]: The constructed delivery options
    """
    do = {}

    reader_type = get_reader_type(request)

    do["reader_type"] = reader_type

    do_dict = read_delivery_options(settings.DELIVERY_OPTIONS_CONFIG)

    # To do: The doptions list contains zero or more dictionaries. Only 1 should be
    # allowed, so fail on zero or greater than 1

    # Surrogate links is always present as a list, which can be empty
    do["do_surrogate"], do["do_av_media"] = surrogate_link_builder(
        doptions[0]["surrogateLinks"]
    )

    # if surrogate links is not an empty list, it will contain one or more dictionaries of the form:
    """     {
                "xReferenceId": null,
                "xReferenceCode": null,
                "xReferenceName": null,
                "xReferenceType": "DIGITIZED_DISCOVERY",
                "xReferenceURL": "<a target=\"_blank\" href=\"https://www.thegenealogist.co.uk/non-conformist-records\">The Genealogist</a>",
                "xReferenceDescription": null,
                "xReferenceSortWord": null
            },
    """

    if doptions[0]["options"] == AvailabilityCondition.ClosedRetainedDeptKnown:
        # Special case. Sometimes, for record type 14 (ClosedRetainedDeptKnown), the department name does not match
        # any entry in the DEPARTMENT_DETAILS dictionary. This shouldn't happen but it does. Therefore, reset the type
        # with that for AvailabilityCondition.ClosedRetainedDeptUnKnown
        if not get_dept(record.reference_number, "deptname"):
            doptions[0][
                "options"
            ] = AvailabilityCondition.ClosedRetainedDeptUnKnown

    # Get the specific delivery option for this artefact
    delivery_option = get_record(do_dict, doptions[0]["options"])

    reader_option = delivery_option["readertype"][reader_type]

    # The reader_option has the following fields:
    #   reader - (staffin/onsitepublic/subsription/offsite) - mandatory
    #   description - is a list of one or more dictionaries containing name and value fields - optional
    #       NOTE: there is a special case when the description name is 'descriptionDCS' - this is for distressing material
    #   heading - string - optional.
    #   orderbuttons - a string containing html for buttons in an unordered list - optional
    #   supplementalcontent - is a list of one or more dictionaries containing name and value fields - optional

    if title := reader_option.get("heading"):
        do["do_heading"] = heading_builder(title, record, do["do_surrogate"])

    if text := reader_option.get("description"):
        do["do_description"] = description_builder(
            text, record, do["do_surrogate"]
        )

    if supp := reader_option.get("supplementalcontent"):
        do["do_supplemental"] = supplemental_builder(
            supp, record, do["do_surrogate"]
        )

    if obutton := reader_option.get("orderbuttons"):
        do["do_orderbuttons"] = orderbuttons_builder(
            obutton, record, do["do_surrogate"]
        )

    if expand := reader_option.get("expandlink"):
        do["do_expandlink"] = expandlink_builder(expand, record)

    if basket := reader_option.get("basketlimit"):
        do["do_basketlimit"] = basketlimit_builder(basket, record)

    return do
