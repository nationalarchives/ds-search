from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Bucket:
    """
    A structured model that holds information that is made available in the templates
    for the user to explore.
    Ex TNA-Records at the National Archives
    """

    key: str
    label: str
    description: str
    href: str = "#"
    record_count: int = 0
    is_current: bool = False


class BucketKeys(StrEnum):
    """
    Keys which represent API data that can be queried.
    """

    TNA = "tna"
    DIGITISED = "digitised"
    NONTNA = "nonTna"


# Configure list of buckets to show in template, these values rarely change
CATALOGUE_BUCKETS = [
    Bucket(
        key=BucketKeys.TNA,
        label="Records at the National Archives",
        description="Results for records held at The National Archives that match your search term.",
    ),
    Bucket(
        key=BucketKeys.DIGITISED,
        label="Online records at The National Archives",
        description="Results for records available to download and held at The National Archives that match your search term.",
    ),
    Bucket(
        key=BucketKeys.NONTNA,
        label="Records at other UK archives",
        description="Results for records held at other archives in the UK (and not at The National Archives) that match your search term.",
    ),
]
