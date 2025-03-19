"""
Constants module for the Django app.
Contains enumerations and fixed values used throughout the application.
"""

from enum import IntEnum

import app.deliveryoptions.helpers as h

class Reader(IntEnum):
    """
    Enumeration representing different types of users/readers accessing the system.
    Used to determine user permissions and available functionalities.
    """
    UNDEFINED = -1    # Default value when reader type cannot be determined
    STAFFIN = 0       # Staff members within the organization
    ONSITEPUBLIC = 1  # Public users physically present at the facility
    SUBSCRIPTION = 2  # Users with a paid subscription
    OFFSITE = 3       # Remote users with no special access


class AvailabilityCondition(IntEnum):
    """
    Enumeration representing different availability conditions for records.
    Used to determine how records can be accessed or delivered to users.
    """
    InvigilationSafeRoom = 0          # Record accessible under supervision in safe room
    CollectionCare = 1                # Record requires special handling in Collection Care
    InUse = 2                         # Record is currently in use by another user
    DigitizedDiscovery = 3            # Digitized record available for discovery
    DigitizedLia = 4                  # Digitized record available through LIA
    DigitizedOther = 5                # Digitized record available through other means
    DigitizedAvailableButNotDownloadableAtPieceLevel = 6  # Digitized but not available for individual download
    DigitizedAvailableButNotDownloadableAtItemLevel = 7   # Digitized but not available for item-level download
    DigitizedPartiallyOpened = 8      # Digitized record partially available
    AV_Media = 9                      # Audio/visual media
    AcademicSubscription = 10         # Available through academic subscription
    ImageLibrary = 11                 # Available in image library
    ClosedFOIReview = 12              # Closed, but can be reviewed via FOI request
    AccessUnderReview = 13            # Access is currently under review
    ClosedRetainedDeptKnown = 14      # Closed and retained by a known department
    ClosedRetainedDeptUnKnown = 15    # Closed and retained by an unknown department
    PaidSearch = 16                   # Available through paid search
    Offsite = 17                      # Record is stored offsite
    Surrogate = 18                    # Surrogate version is available
    Unfit = 19                        # Record is unfit for production
    MouldTreatment = 20               # Record requires mould treatment
    Onloan = 21                       # Record is on loan to another organization
    DisplayAtMuseum = 22              # Record is on display at a museum
    MissingLost = 23                  # Record is missing or lost
    GovtWebArchive = 24               # Record is in the government web archive
    LocalArchive = 25                 # Record is in a local archive
    OrderOriginal = 26                # Original record can be ordered
    FileAuthority = 27                # Related to file authority
    TooLargeToCopyOriginal = 28       # Original too large to copy
    TooLargeToCopyOffsite = 29        # Offsite record too large to copy
    TooLargeToCopySurrogate = 30      # Surrogate too large to copy
    UnAvailable = 31                  # Record is unavailable
    OrderException = 32               # Exception in ordering process
    AdvanceOrderOnly = 33             # Available for advance order only
    Relocation = 34                   # Record is being relocated


# IP address ranges for identifying staff members within the organization
IP_STAFFIN_RANGES = [
    {"Address": "172.31.8.0/22", "Description": "Front-end Web servers"},
    {
        "Address": "10.96.0.0/13",
        "Description": "UPTOS servers- all NA- servers",
    },
    {
        "Address": "10.104.0.0/13",
        "Description": "Staff Edge User Access",
    },
    {
        "Address": "10.95.48.0/24",
        "Description": "TNA WVD",
    },
    {
        "Address": "172.31.0.0/21",
        "Description": "BIA Excluding web servers and load balanced services",
    },
    {
        "Address": "10.252.16.0/21",
        "Description": "Staff Remote Access",
    },
    {
        "Address": "10.252.21.0/24",
        "Description": "F5 VPN Staff Remote Access",
    },
    {
        "Address": "10.114.1.0/24",
        "Description": "F5 BIG-IP",
    },
]

# IP address ranges for identifying on-site public users
IP_ONSITE_RANGES = [
    {
        "Address": "10.136.0.0/19",
        "Description": "Public reading rooms device (Thin clients and PCs) VLAN",
    },
    {
        "Address": "167.98.93.94/32",
        "Description": "Public Wi-Fi",
    },
    {
        "Address": "10.120.0.0/13",
        "Description": "Public Edge User Access",
    },
    {
        "Address": "10.112.0.0/13",
        "Description": "Untrusted servers- all WB- servers ( including reading rooms thin client pcs incl staff and public wifi)",
    },
]


# Mapping of template tags to their corresponding helper functions
# These are used to replace placeholders in HTML templates with dynamic content
deliveryOptionsTags = {
    "{AccessConditionText}": h.get_access_condition_text,
    "{AddedToBasketText}": h.get_added_to_basket_text,
    "{AdvancedOrdersEmailAddress}": h.get_advanced_orders_email_address,
    "{AdvanceOrderInformationUrl}": h.get_advance_order_information,
    "{ArchiveLink}": h.get_archive_link,
    "{ArchiveName}": h.get_archive_name,
    "{BasketType}": h.get_basket_type,
    "{BasketUrl}": h.get_basket_url,
    "{BrowseUrl}": h.get_browse_url,
    "{ContactFormUrlUnfit}": h.get_contact_form_url_unfit,
    "{ContactFormUrlMould}": h.get_contact_form_url_mould,
    "{ContactFormUrl}": h.get_contact_form_url,
    "{DataProtectionActUrl}": h.get_data_protection_act_url,
    "{DeptName}": h.get_dept_name,
    "{DeptUrl}": h.get_dept_url,
    "{DownloadFormat}": h.get_download_format,
    "{DownloadText}": h.get_download_text,
    "{DownloadUrl}": h.get_download_url,
    "{FAType}": h.get_file_authority_type,
    "{FoiUrl}": h.get_foi_url,
    "{ImageLibraryUrl}": h.get_image_library_url,
    "{ItemNumOfFilesAndSizeInMB}": h.get_item_num_of_files_and_size_in_MB,
    "{KeepersGalleryUrl}": h.get_keepers_gallery_url,
    "{KewBookingSystemUrl}": h.get_kew_booking_system_url,
    "{MaxItems}": h.get_max_items,
    "{OpenDateDesc}": h.get_open_date_desc,
    "{OpeningTimesUrl}": h.get_opening_times_url,
    "{OrderUrl}": h.get_order_url,
    "{PaidSearchUrl}": h.get_paid_search_url,
    "{Price}": h.get_price,
    "{ReadersTicketUrl}": h.get_readers_ticket_url,
    "{RecordCopyingUrl}": h.get_record_copying_url,
    "{RecordInformationType}": h.get_record_information_type,
    "{RecordOpeningDate}": h.get_record_opening_date,
    "{RecordUrl}": h.get_record_url,
    "{AllWebsiteUrls}": h.get_all_website_urls,
    "{SubsWebsiteUrls}": h.get_subsequent_website_urls,
    "{FirstWebsiteUrl}": h.get_first_website_url,
    "{FirstWebsiteUrlFull}": h.get_first_website_url_full,
    "{WebsiteUrlText}": h.get_website_url_text,
    "{YourOrderLink}": h.get_your_order_link,
}