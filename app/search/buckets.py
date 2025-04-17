import copy
from dataclasses import dataclass
from enum import StrEnum
from typing import List

from django.contrib.humanize.templatetags.humanize import intcomma


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

    @property
    def label_with_count(self):
        if self.record_count is None:
            return self.label
        return self.label + f" ({intcomma(self.record_count)})"

    @property
    def for_display(self):
        """
        Returns data formatted for front-end component Ex: tnaSecondaryNavigation()
        """
        return {
            "name": self.label_with_count,
            "href": self.href,
            "current": self.is_current,
        }


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


def get_buckets_for_display(
    query: str, buckets: dict, current_bucket_key: str
) -> list:
    """
    Returns modified buckets data to be used in the template
    by front-end component Ex: tnaSecondaryNavigation()
    """
    # new list that is modified
    bucket_list = copy.deepcopy(CATALOGUE_BUCKETS)

    # update buckets from params
    for bucket in bucket_list:
        bucket.record_count = buckets.get(bucket.key, 0)
        bucket.is_current = bucket.key == current_bucket_key
        if bucket.href == "#":
            bucket.href = f"?group={bucket.key}"
            if query:
                bucket.href += f"&q={query}"

    # return data for display
    return [bucket.for_display for bucket in bucket_list]
