"""
Helper functions module for the Django app.
Contains functions to replace template placeholders with dynamic content.
These functions are used in the deliveryOptionsTags dictionary.
"""

import re
from typing import List, Optional, Any

from django.conf import settings
from django.core.cache import cache

from app.deliveryoptions.departments import DEPARTMENT_DETAILS
from app.records.models import Record

def get_dept(reference_number: str, field: str) -> Optional[str]:
    """
    Get department information from a reference number.
    
    The reference_number is the entire reference, e.g. "PROB 11/1022/1" or "RAIL 1005/190"
    We are looking to see if the first x characters of the reference_number match the key in
    the dept_details dictionary.

    Args:
        reference_number: The full reference number
        field: The key to retrieve, either 'deptname' or 'depturl'
    
    Returns:
        The value for the specified field from the matching department or None if not found
    """
    # Create a cache key based on the parameters
    cache_key = f"dept_{reference_number}_{field}"
    
    # Try to get the result from the cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    
    # If not in cache, compute the result
    result = None
    for key, value in DEPARTMENT_DETAILS.items():
        if reference_number.startswith(key):
            result = value[field]
            break
    
    # Store the result in the cache (default timeout)
    cache.set(cache_key, result)
    
    return result

def get_access_condition_text(record: Record, surrogate: List) -> str:
    """
    Get the access condition text for a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The access condition text or a space if none exists
    """
    if ac := record.access_condition:  # If it's not None, return it
        return ac
    return " "


def get_added_to_basket_text(record: Record, surrogate: List) -> str:
    """
    Get the text to display for adding to basket.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The text for the add to basket button
    """
    return "Add to basket"


def get_advanced_orders_email_address(record: Record, surrogate: List) -> str:
    """
    Get the email address for advanced orders.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The email address for advanced document orders
    """
    return settings.ADVANCED_DOCUMENT_ORDER_EMAIL


def get_advance_order_information(record: Record, surrogate: List) -> str:
    """
    Get the URL for advance order information.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for advance order information
    """
    return f"{settings.BASE_TNA_URL}/about/visit-us/"


def get_archive_link(record: Record, surrogate: List) -> str:
    """
    Get the link to the archive holding the record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL of the archive holding the record
    """
    return record.held_by_url


def get_archive_name(record: Record, surrogate: List) -> str:
    """
    Get the name of the archive holding the record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The name of the archive holding the record
    """
    return record.held_by


def get_basket_type(record: Record, surrogate: List) -> str:
    """
    Get the basket type.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The basket type (e.g., "Digital Downloads")
    """
    # Covered originally in ticket EDEV-113. Assumed to be 'Digital Downloads'
    return "Digital Downloads"


def get_basket_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the basket.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the basket
    """
    return f"{settings.BASE_TNA_URL}/basket/"


def get_browse_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for browsing the record hierarchy.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for browsing the record hierarchy
    """
    # This will be the browse URL for the hierarchy we are currently in.
    # On Discovery, an example would be https://discovery.nationalarchives.gov.uk/browse/r/h/C325982
    return f"{settings.BASE_TNA_URL}/browse/tbd/{record.iaid}/"


def get_contact_form_url_mould(record: Record, surrogate: List) -> str:
    """
    Get the URL for the contact form for records needing mould treatment.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the mould treatment contact form
    """
    return f"{get_contact_form_url(record, surrogate)}document-condition-feedback/?catalogue-reference={record.reference_number}&mould-treatment-required=true"


def get_contact_form_url_unfit(record: Record, surrogate: List) -> str:
    """
    Get the URL for the contact form for unfit records.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the unfit record contact form
    """
    return f"{get_contact_form_url(record, surrogate)}document-condition-feedback/?catalogue-reference={record.reference_number}&conservation-treatment-required=true"


def get_contact_form_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the general contact form.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the general contact form
    """
    return f"{settings.BASE_TNA_URL}/contact-us/"


def get_data_protection_act_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the Data Protection Act information.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the Data Protection Act information
    """
    return f"{settings.BASE_TNA_URL}/content/documents/county-durham-home-guard-service-record-subject-access-request-form.pdf"


def get_dept_name(record: Record, surrogate: List) -> str:
    """
    Get the name of the department responsible for a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The name of the department or empty string if not found
    """
    if name := get_dept(record.reference_number, "deptname"):
        return name
    else:
        return ""


def get_dept_url(record: Record, surrogate: List) -> str:
    """
    Get the URL of the department responsible for a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL of the department or empty string if not found
    """
    if url := get_dept(record.reference_number, "depturl"):
        return url
    else:
        return ""


def get_dept(reference_number: str, field: str) -> Optional[str]:
    """
    Get department information from a reference number.
    
    Args:
        reference_number: The full reference number (e.g., "PROB 11/1022/1")
        field: The field to retrieve (either 'deptname' or 'depturl')
        
    Returns:
        The requested department field value or None if not found
    """
    for key, value in DEPARTMENT_DETAILS.items():
        if reference_number.startswith(key):
            return value[field]

    return None


def get_download_format(record: Record, surrogate: List) -> str:
    """
    Get the download format for a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The download format (e.g., "PDF" or "ZIP")
    """
    # PDF or ZIP file - in Discovery, defined in discovery/RDWeb/Services/Mapper/DeliveryOptionsMapper.cs
    return "(Unknown download format)"


def get_download_text(record: Record, surrogate: List) -> str:
    """
    Get the text for the download button.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The text for the download button
    """
    return "Download now"


def get_download_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for downloading a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for downloading the record
    """
    return "details/download"


def get_file_authority_type(record: Record, surrogate: List) -> str:
    """
    Get the file authority type.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The file authority type
    """
    # Unknown derivation - EDEV-111. We don't think it is needed, so setting to blank
    return " "


def get_foi_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for submitting a Freedom of Information request.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for submitting an FOI request for this record
    """
    return f"{settings.BASE_TNA_URL}/foirequest?reference={record.reference_number}"


def get_image_library_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the image library.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the image library
    """
    return settings.IMAGE_LIBRARY_URL


def get_item_num_of_files_and_size_in_MB(record: Record, surrogate: List) -> str:
    """
    Get the number of files and total size for a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        A string describing the number of files and size in MB
    """
    # On Discovery this is held in Mongo - no equivalent is yet available on Rosetta
    return "(Unknown number of files and file size)"


def get_keepers_gallery_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the Keepers' Gallery.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the Keepers' Gallery
    """
    return f"{settings.BASE_TNA_URL}/about/visit-us/whats-on/keepers-gallery/"


def get_kew_booking_system_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the Kew booking system.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the Kew booking system
    """
    return f"{settings.BASE_TNA_URL}/book-a-reading-room-visit/"


def get_max_items(record: Record, surrogate: List) -> str:
    """
    Get the maximum number of items allowed in a basket.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The maximum number of items allowed
    """
    return settings.MAX_BASKET_ITEMS


def get_open_date_desc(record: Record, surrogate: List) -> str:
    """
    Get the description for the record opening date.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The text "Opening date: " if a record opening date exists, otherwise a space
    """
    if record.record_opening:
        return "Opening date: "
    return " "


def get_opening_times_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the opening times information.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for opening times information
    """
    return f"{settings.BASE_TNA_URL}/about/visit-us/"


def get_order_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for ordering a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for ordering the record
    """
    # On Discovery, this is related to cookie settings for a DORIS cookie.
    return "Order URL not yet available"


def get_paid_search_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for paid search options.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for paid search options for this record
    """
    return f"{settings.BASE_TNA_URL}/paidsearch/foirequest/{record.iaid}?type=foirequest"


def get_price(record: Record, surrogate: List) -> str:
    """
    Get the price for a record.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The price for the record
    """
    # EDEV-109
    return "(Unknown price)"


def get_readers_ticket_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for information about reader's tickets.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for reader's ticket information
    """
    return f"{settings.BASE_TNA_URL}/about/visit-us/researching-here/do-i-need-a-readers-ticket/"


def get_record_copying_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for the record copying service.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for the record copying service
    """
    return f"{settings.DISCOVERY_TNA_URL}/pagecheck/start/{record.iaid}/"


def get_record_information_type(record: Record, surrogate: List) -> str:
    """
    Get the record information type.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The record information type
    """
    # EDEV-110
    return "(Unknown record information type)"


def get_record_opening_date(record: Record, surrogate: List) -> str:
    """
    Get the record opening date.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The record opening date or a space if none exists
    """
    if rod := record.record_opening:
        return rod
    return " "


def get_record_url(record: Record, surrogate: List) -> str:
    """
    Get the URL for viewing a record's details.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL for viewing the record's details
    """
    # Subject to change once ds-detail is fleshed out
    return f"{settings.BASE_TNA_URL}/details/r/{record.iaid}/"


def get_first_website_url(record: Record, surrogate: List) -> str:
    """
    Get the URL of the first website in the surrogate list.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The URL of the first website or empty string if none exists
    """
    # This comes from the delivery options surrogate dictionary. They all have html markup
    # embedded in them but this particular case is for a button, so we need to extract the
    # href from the string.
    if len(surrogate) > 0:
        match = re.search(r'href="([^"]+)"', surrogate[0])

        return match.group(1) if match else ""
    else:
        return ""


def get_first_website_url_full(record: Record, surrogate: List) -> str:
    """
    Get the full HTML for the first website in the surrogate list.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The full HTML for the first website or empty string if none exists
    """
    if len(surrogate) > 0:
        return surrogate[0]
    else:
        return ""


def get_subsequent_website_urls(record: Record, surrogate: List) -> str:
    """
    Get HTML for all websites in the surrogate list except the first one.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        HTML for all websites except the first one
    """
    st = " "
    if len(surrogate) > 1:
        for s in surrogate[1:]:
            st += "<li>" + s + "</li>"
    return st


def get_all_website_urls(record: Record, surrogate: List) -> str:
    """
    Get HTML for all websites in the surrogate list.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        HTML for all websites in the surrogate list
    """
    st = " "
    for s in surrogate:
        st += "<li>" + s + "</li>"
    return st


def get_website_url_text(record: Record, surrogate: List) -> str:
    """
    Get the text from the first website URL in the surrogate list.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The text from the first website URL or a space if none exists
    """
    pattern = r">(.*?)<"

    if len(surrogate):
        match = re.search(pattern, surrogate[0])
        return match.group(1) if match else ""
    else:
        return " "


def get_your_order_link(record: Record, surrogate: List) -> str:
    """
    Get the link to the user's current order.
    
    Args:
        record: The record object
        surrogate: List of surrogate data
        
    Returns:
        The link to the user's current order
    """
    return "(Unknown order link)"