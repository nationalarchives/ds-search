import json
import os
from enum import IntEnum

import app.deliveryoptions.helpers as h


class Reader(IntEnum):
    """
    Enumeration representing different types of users/readers accessing the system.
    Used to determine user permissions and available functionalities.
    """

    UNDEFINED = -1  # Default value when reader type cannot be determined
    STAFFIN = 0  # Staff members within the organization
    ONSITEPUBLIC = 1  # Public users physically present at the facility
    SUBSCRIPTION = 2  # Users with a paid subscription
    OFFSITE = 3  # Remote users with no special access


class AvailabilityCondition(IntEnum):
    """
    Enumeration representing different availability conditions for records.
    Used to determine how records can be accessed or delivered to users.
    """

    InvigilationSafeRoom = 0  # Record accessible under supervision in safe room
    CollectionCare = 1  # Record requires special handling in Collection Care
    InUse = 2  # Record is currently in use by another user
    DigitizedDiscovery = 3  # Digitized record available for discovery
    DigitizedLia = 4  # Digitized record available through LIA
    DigitizedOther = 5  # Digitized record available through other means
    DigitizedAvailableButNotDownloadableAtPieceLevel = (
        6  # Digitized but not available for individual download
    )
    DigitizedAvailableButNotDownloadableAtItemLevel = (
        7  # Digitized but not available for item-level download
    )
    DigitizedPartiallyOpened = 8  # Digitized record partially available
    AV_Media = 9  # Audio/visual media
    AcademicSubscription = 10  # Available through academic subscription
    ImageLibrary = 11  # Available in image library
    ClosedFOIReview = 12  # Closed, but can be reviewed via FOI request
    AccessUnderReview = 13  # Access is currently under review
    ClosedRetainedDeptKnown = 14  # Closed and retained by a known department
    ClosedRetainedDeptUnKnown = (
        15  # Closed and retained by an unknown department
    )
    PaidSearch = 16  # Available through paid search
    Offsite = 17  # Record is stored offsite
    Surrogate = 18  # Surrogate version is available
    Unfit = 19  # Record is unfit for production
    MouldTreatment = 20  # Record requires mould treatment
    Onloan = 21  # Record is on loan to another organization
    DisplayAtMuseum = 22  # Record is on display at a museum
    MissingLost = 23  # Record is missing or lost
    GovtWebArchive = 24  # Record is in the government web archive
    LocalArchive = 25  # Record is in a local archive
    OrderOriginal = 26  # Original record can be ordered
    FileAuthority = 27  # Related to file authority
    TooLargeToCopyOriginal = 28  # Original too large to copy
    TooLargeToCopyOffsite = 29  # Offsite record too large to copy
    TooLargeToCopySurrogate = 30  # Surrogate too large to copy
    UnAvailable = 31  # Record is unavailable
    OrderException = 32  # Exception in ordering process
    AdvanceOrderOnly = 33  # Available for advance order only
    Relocation = 34  # Record is being relocated


# IP address ranges for identifying staff members within the organization
IP_STAFFIN_RANGES = json.loads(os.getenv("IP_STAFFIN_RANGES", "[]"))

# IP address ranges for identifying on-site public users
IP_ONSITE_RANGES = json.loads(os.getenv("IP_ONSITE_RANGES", "[]"))

# Distressing content prefixes
DCS_PREFIXES = [
    item.strip()
    for item in os.getenv("DELIVERY_OPTIONS_DCS_LIST", "").split(",")
    if item.strip()
]

# Mapping of template tags to their corresponding helper functions
# These are used to replace placeholders in HTML templates with dynamic content
delivery_option_tags = {
    "{AccessConditionText}": h.helper_get_access_condition_text,
    "{AddedToBasketText}": h.helper_get_added_to_basket_text,
    "{AdvancedOrdersEmailAddress}": h.helper_get_advanced_orders_email_address,
    "{AdvanceOrderInformationUrl}": h.helper_get_advance_order_information,
    "{ArchiveLink}": h.helper_get_archive_link,
    "{ArchiveName}": h.helper_get_archive_name,
    "{BasketType}": h.helper_get_basket_type,
    "{BasketUrl}": h.helper_get_basket_url,
    "{BrowseUrl}": h.helper_get_browse_url,
    "{ContactFormUrlUnfit}": h.helper_get_contact_form_url_unfit,
    "{ContactFormUrlMould}": h.helper_get_contact_form_url_mould,
    "{ContactFormUrl}": h.helper_get_contact_form_url,
    "{DataProtectionActUrl}": h.helper_get_data_protection_act_url,
    "{DeptName}": h.helper_get_dept_name,
    "{DeptUrl}": h.helper_get_dept_url,
    "{DownloadFormat}": h.helper_get_download_format,
    "{DownloadText}": h.helper_get_download_text,
    "{DownloadUrl}": h.helper_get_download_url,
    "{FAType}": h.helper_get_file_authority_type,
    "{FoiUrl}": h.helper_get_foi_url,
    "{ImageLibraryUrl}": h.helper_get_image_library_url,
    "{ItemNumOfFilesAndSizeInMB}": h.helper_get_item_num_of_files_and_size_in_MB,
    "{KeepersGalleryUrl}": h.helper_get_keepers_gallery_url,
    "{KewBookingSystemUrl}": h.helper_get_kew_booking_system_url,
    "{MaxItems}": h.helper_get_max_items,
    "{OpenDateDesc}": h.helper_get_open_date_desc,
    "{OpeningTimesUrl}": h.helper_get_opening_times_url,
    "{OrderUrl}": h.helper_get_order_url,
    "{PaidSearchUrl}": h.helper_get_paid_search_url,
    "{Price}": h.helper_get_price,
    "{ReadersTicketUrl}": h.helper_get_readers_ticket_url,
    "{RecordCopyingUrl}": h.helper_get_record_copying_url,
    "{RecordInformationType}": h.helper_get_record_information_type,
    "{RecordOpeningDate}": h.helper_get_record_opening_date,
    "{RecordUrl}": h.helper_get_record_url,
    "{AllWebsiteUrls}": h.helper_get_all_website_urls,
    "{SubsWebsiteUrls}": h.helper_get_subsequent_website_urls,
    "{FirstWebsiteUrl}": h.helper_get_first_website_url,
    "{FirstWebsiteUrlFull}": h.helper_get_first_website_url_full,
    "{WebsiteUrlText}": h.helper_get_website_url_text,
    "{YourOrderLink}": h.helper_get_your_order_link,
}
