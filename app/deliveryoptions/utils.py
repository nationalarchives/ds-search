import json
import re

from enum import IntEnum
from functools import cache
from typing import Any, Dict, List, Tuple, Union

from django.conf import settings


class Reader(IntEnum):
    STAFFIN = 0
    ONSITEPUBLIC = 1
    SUBSCRIPTION = 2
    OFFSITE = 3


class AvailabilityCondition(IntEnum):
    InvigilationSafeRoom = 0
    CollectionCare = 1
    InUse = 2
    DigitizedDiscovery = 3
    DigitizedLia = 4
    DigitizedOther = 5
    DigitizedAvailableButNotDownloadableAtPieceLevel = 6
    DigitizedAvailableButNotDownloadableAtItemLevel = 7
    DigitizedPartiallyOpened = 8
    AV_Media = 9
    AcademicSubscription = 10
    ImageLibrary = 11
    ClosedFOIReview = 12
    AccessUnderReview = 13
    ClosedRetainedDeptKnown = 14
    ClosedRetainedDeptUnKnown = 15
    PaidSearch = 16
    Offsite = 17
    Surrogate = 18
    Unfit = 19
    MouldTreatment = 20
    Onloan = 21
    DisplayAtMuseum = 22
    MissingLost = 23
    GovtWebArchive = 24
    LocalArchive = 25
    OrderOriginal = 26
    FileAuthority = 27
    TooLargeToCopyOriginal = 28
    TooLargeToCopyOffsite = 29
    TooLargeToCopySurrogate = 30
    UnAvailable = 31
    OrderException = 32
    AdvanceOrderOnly = 33
    Relocation = 34


dept_details = {
    "AB": {
        "deptname": "Nuclear Decommissioning Authority",
        "depturl": "https://www.gov.uk/government/organisations/nuclear-decommissioning-authority",
    },
    "ADM": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "AIR": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "CAB": {
        "deptname": "Cabinet Office",
        "depturl": "http://www.cabinetoffice.gov.uk/content/freedom-information-foi",
    },
    "CO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "COAL": {
        "deptname": "Department for Business, Energy and Industrial Strategy",
        "depturl": "https://www.gov.uk/government/organisations/department-for-business-energy-and-industrial-strategy",
    },
    "DEFE": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "DO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "ES": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "FCO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "FO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "PREM": {
        "deptname": "Cabinet Office",
        "depturl": "http://www.cabinetoffice.gov.uk/content/freedom-information-foi",
    },
    "T 352": {
        "deptname": "Cabinet Office",
        "depturl": "http://www.cabinetoffice.gov.uk/content/freedom-information-foi",
    },
    "WO": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    # Add more departments as needed
}


@cache
def get_dept(reference_number: str, field: str):
    """
    The reference_number is the entire reference, e.g. "PROB 11/1022/1" or "RAIL 1005/190"
    We are looking to see if the first x characters of the reference_number match the key in
    the dept_details dictionary above.

    The key is either 'deptname' or 'depturl'
    """

    for key, value in dept_details.items():
        if reference_number.startswith(key):
            return value[field]

    return None


"""
    Helper functions that provide the logic to return values for {xyz} tags in the delivery_options.json file.
    Some are simple urls or text strings, others require data from elsewhere in order to calculate them.
"""


def get_access_condition_text(record: dict, surrogate: List) -> str:
    if ac := record.access_condition:  # If it's not None, return it
        return ac
    return " "


def get_added_to_basket_text(record: dict, surrogate: List) -> str:
    return "Add to basket"


def get_advanced_orders_email_address(record: dict, surrogate: List) -> str:
    return "mailto:advanceddocumentorder@nationalarchives.gov.uk"


def get_advance_order_information(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_TNA_URL}/about/visit-us/"


def get_archive_link(record: dict, surrogate: List) -> str:
    return record.held_by_url


def get_archive_name(record: dict, surrogate: List) -> str:
    return record.held_by


def get_basket_type(record: dict, surrogate: List) -> str:  # Unknown derivation
    return "(EDEV-113)"


def get_basket_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_DISCOVERY_URL}/basket/"


def get_browse_url(record: dict, surrogate: List) -> str:  # Unknown derivation
    return "(EDEV-112)"


def get_contact_form_url_mould(record: dict, surrogate: List) -> str:
    return f"{get_contact_form_url(record, surrogate)}document-condition-feedback/?catalogue-reference={record.reference_number}&mould-treatment-required=true"


def get_contact_form_url_unfit(record: dict, surrogate: List) -> str:
    return f"{get_contact_form_url(record, surrogate)}document-condition-feedback/?catalogue-reference={record.reference_number}&conservation-treatment-required=true"


def get_contact_form_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_TNA_URL}/contact-us/"


def get_data_protection_act_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_DISCOVERY_URL}/Content/documents/county-durham-home-guard-service-record-subject-access-request-form.pdf"


def get_dept_name(record: dict, surrogate: List) -> str:
    if name := get_dept(record.reference_number, "deptname"):
        return name
    else:
        return ""


def get_dept_url(record: dict, surrogate: List) -> str:
    if url := get_dept(record.reference_number, "depturl"):
        return url
    else:
        return ""


def get_download_format(record: dict, surrogate: List) -> str:
    return "(EDEV-108)"


def get_download_text(record: dict, surrogate: List) -> str:
    return "Download now"


def get_download_url(record: dict, surrogate: List) -> str:
    return "details/download"


def get_file_authority_type(record: dict, surrogate: List) -> str:  # Unknown derivation
    return "(EDEV-111)"


def get_foi_url(record: dict, surrogate: List) -> str:
    return (
        f"{settings.BASE_DISCOVERY_URL}/foirequest?reference={record.reference_number}"
    )


def get_image_library_url(record: dict, surrogate: List) -> str:
    return "https://images.nationalarchives.gov.uk/"


def get_item_num_of_files_and_size_in_MB(record: dict, surrogate: List) -> str:
    return "(EDEV-107)"


def get_keepers_gallery_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_TNA_URL}/about/visit-us/whats-on/keepers-gallery/"


def get_kew_booking_system_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_TNA_URL}/book-a-reading-room-visit/"


def get_max_items(record: dict, surrogate: List) -> str:
    return settings.MAX_BASKET_ITEMS


def get_open_date_desc(record: dict, surrogate: List) -> str:
    if record.record_opening:
        return "Opening date: "
    return " "


def get_opening_times_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_TNA_URL}/about/visit-us/"


def get_order_url(record: dict, surrogate: List) -> str:
    return "(EDEV-113)"


def get_paid_search_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_DISCOVERY_URL}/paidsearch/foirequest/{record.iaid}?type=foirequest"


def get_price(record: dict, surrogate: List) -> str:
    return "(EDEV-109)"


def get_readers_ticket_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_TNA_URL}/about/visit-us/researching-here/do-i-need-a-readers-ticket/"


def get_record_copying_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_DISCOVERY_URL}/pagecheck/start/{record.iaid}/"


def get_record_information_type(record: dict, surrogate: List) -> str:
    return "(EDEV-110)"


def get_record_opening_date(record: dict, surrogate: List) -> str:
    if rod := record.record_opening:
        return rod
    return " "


def get_record_url(record: dict, surrogate: List) -> str:
    return f"{settings.BASE_DISCOVERY_URL}/details/r/{record.parent.iaid}/"


def get_first_website_url(record: dict, surrogate: List) -> str:
    # This comes from the delivery options surrogate dictionary. They all have html markup
    # embedded in them but this particular case is for a button, so we need to extract the
    # href from the string.
    if len(surrogate) > 0:
        match = re.search(r'href="([^"]+)"', surrogate[0])

        return match.group(1) if match else ""
    else:
        return ""


def get_first_website_url_full(record: dict, surrogate: List) -> str:
    if len(surrogate) > 0:
        return surrogate[0]
    else:
        return ""


def get_subsequent_website_urls(record: dict, surrogate: List) -> str:
    st = " "
    if len(surrogate) > 1:
        for s in surrogate[1:]:
            st += "<li>" + s + "</li>"
    return st


def get_all_website_urls(record: dict, surrogate: List) -> str:
    st = " "
    for s in surrogate:
        st += "<li>" + s + "</li>"
    return st


# Temporary markup
def get_WebsiteUrls(record: dict, surrogate: List) -> str:
    st = " "
    for s in surrogate[1:]:
        st += "<li>" + s + "</li>"
    return st


# Temporary markup
def get_WebsiteUrl(record: dict, surrogate: List) -> str:
    return surrogate[0]


def get_website_url_text(record: dict, surrogate: List) -> str:
    pattern = r">(.*?)<"

    if len(surrogate):
        match = re.search(pattern, surrogate[0])
        return match.group(1) if match else ""
    else:
        return " "


def get_your_order_link(record: dict, surrogate: List) -> str:
    return "(EDEV-113)"


# This dict links the embedded tags with a helper function that returns the
# correct inserted value, e.g. url's
deliveryOptionsTags = {
    "{AccessConditionText}": get_access_condition_text,
    "{AddedToBasketText}": get_added_to_basket_text,
    "{AdvancedOrdersEmailAddress}": get_advanced_orders_email_address,
    "{AdvanceOrderInformationUrl}": get_advance_order_information,
    "{ArchiveLink}": get_archive_link,
    "{ArchiveName}": get_archive_name,
    "{BasketType}": get_basket_type,
    "{BasketUrl}": get_basket_url,
    "{BrowseUrl}": get_browse_url,
    "{ContactFormUrlUnfit}": get_contact_form_url_unfit,
    "{ContactFormUrlMould}": get_contact_form_url_mould,
    "{ContactFormUrl}": get_contact_form_url,
    "{DataProtectionActUrl}": get_data_protection_act_url,
    "{DeptName}": get_dept_name,
    "{DeptUrl}": get_dept_url,
    "{DownloadFormat}": get_download_format,
    "{DownloadText}": get_download_text,
    "{DownloadUrl}": get_download_url,
    "{FAType}": get_file_authority_type,
    "{FoiUrl}": get_foi_url,
    "{ImageLibraryUrl}": get_image_library_url,
    "{ItemNumOfFilesAndSizeInMB}": get_item_num_of_files_and_size_in_MB,
    "{KeepersGalleryUrl}": get_keepers_gallery_url,
    "{KewBookingSystemUrl}": get_kew_booking_system_url,
    "{MaxItems}": get_max_items,
    "{OpenDateDesc}": get_open_date_desc,
    "{OpeningTimesUrl}": get_opening_times_url,
    "{OrderUrl}": get_order_url,
    "{PaidSearchUrl}": get_paid_search_url,
    "{Price}": get_price,
    "{ReadersTicketUrl}": get_readers_ticket_url,
    "{RecordCopyingUrl}": get_record_copying_url,
    "{RecordInformationType}": get_record_information_type,
    "{RecordOpeningDate}": get_record_opening_date,
    "{RecordUrl}": get_record_url,
    "{AllWebsiteUrls}": get_all_website_urls,
    "{SubsWebsiteUrls}": get_subsequent_website_urls,
    "{FirstWebsiteUrl}": get_first_website_url,
    "{FirstWebsiteUrlFull}": get_first_website_url_full,
    "{WebsiteUrlText}": get_website_url_text,
    "{YourOrderLink}": get_your_order_link,
}

# Dictionary to serve as a cache for file contents, preventing redundant file reads
file_cache = {}


def read_delivery_options(file_path: str) -> List:
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


@cache
def get_dcs_prefixes() -> List:
    dcs = settings.DELIVERY_OPTIONS_DCS_LIST
    return dcs.split()


def distressing_content_match(reference: str) -> bool:
    dcs_prefixes = get_dcs_prefixes()

    return list(filter(reference.startswith, dcs_prefixes)) != []


def get_record(cache: Dict, record_id: int):
    try:
        return cache["deliveryOptions"]["option"][record_id]
    except Exception:
        return None


def html_replacer(string: str, record: dict, surrogate_data: List) -> str:
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
    record_data: Dict,
    surrogate_data: List = [],
    dcs: bool = False,
) -> str:
    html = ""

    if delivery_option_data is None:
        return html

    if isinstance(delivery_option_data, list):
        for item in delivery_option_data:
            if not dcs and item["name"] == "descriptionDCS":
                pass
            else:
                html += html_replacer(item["value"], record_data, surrogate_data)
    else:
        html = html_replacer(delivery_option_data, record_data, surrogate_data)

    return html


# Specific pre-processing for the order buttons data
def orderbuttons_builder(
    delivery_option_data: List, record_data: Dict, surrogate_data: List
) -> List:
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
    delivery_option_data: Union[List, str], record_data: Dict
) -> str:
    return html_builder(delivery_option_data, record_data)


# Specific pre-processing for the expand link data
def expandlink_builder(
    delivery_option_data: Union[List, str], record_data: Dict
) -> str:
    return html_builder(delivery_option_data, record_data)


# Specific pre-processing for the description data
def description_builder(
    delivery_option_data: Union[List, str], record_data: Dict, surrogate_data: List
) -> str:
    if distressing_content_match(record_data.reference_number):
        return html_builder(
            delivery_option_data, record_data, surrogate_data=surrogate_data, dcs=True
        )

    return html_builder(
        delivery_option_data, record_data, surrogate_data=surrogate_data
    )


# Specific pre-processing for the supplemental data
def supplemental_builder(
    delivery_option_data: Union[List, str], record_data: Dict, surrogate_data: List
) -> str:
    return html_builder(
        delivery_option_data, record_data, surrogate_data=surrogate_data
    )


# Specific pre-processing for the heading
def heading_builder(
    delivery_option_data: str, record_data: Dict, surrogate_data: List
) -> str:
    return html_builder(
        delivery_option_data, record_data, surrogate_data=surrogate_data
    )


def surrogate_link_builder(surrogates: List) -> Tuple[List[Any], List[Any]]:
    surrogate_list = []
    av_media_list = []

    for s in surrogates:
        surrogate_list.append(s["xReferenceURL"])

        if s["xReferenceType"] == "AV_MEDIA":
            av_media_list.append(s["xReferenceURL"])

    return surrogate_list, av_media_list


""" The following four functions are used to determine the reader type. These are
to be written under ticket EDEV-115 when enough is known about the mechanism """


def is_onsite() -> bool:
    return False


def is_subscribed() -> bool:
    return False


def is_staff() -> bool:
    return False


def get_reader_type() -> Reader:
    # EDEV-115
    # Code to determine status of reader (see enum Reader above).
    reader = Reader.OFFSITE

    if is_subscribed():
        reader = Reader.SUBSCRIPTION
    elif is_onsite():
        reader = Reader.ONSITEPUBLIC
    elif is_staff():
        reader = Reader.STAFFIN

    return reader


""" End of EDEV-115 """


# Main routine called from records.py
def construct_delivery_options(doptions: list, record: dict) -> dict:
    do = {}

    # EDEV-115
    reader_type = get_reader_type()

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
        # any entry in the dept_details dictionary above. This shouldn't happen but it does. Therefore, reset the type
        # with that for AvailabilityCondition.ClosedRetainedDeptUnKnown
        if not get_dept(record.reference_number, "deptname"):
            doptions[0]["options"] = AvailabilityCondition.ClosedRetainedDeptUnKnown

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
        do["do_description"] = description_builder(text, record, do["do_surrogate"])

    if supp := reader_option.get("supplementalcontent"):
        do["do_supplemental"] = supplemental_builder(supp, record, do["do_surrogate"])

    if obutton := reader_option.get("orderbuttons"):
        do["do_orderbuttons"] = orderbuttons_builder(obutton, record, do["do_surrogate"])

    if expand := reader_option.get("expandlink"):
        do["do_expandlink"] = expandlink_builder(expand, record)

    if basket := reader_option.get("basketlimit"):
        do["do_basketlimit"] = basketlimit_builder(basket, record)

    return do
