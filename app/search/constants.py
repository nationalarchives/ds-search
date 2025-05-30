from enum import StrEnum


class Sort(StrEnum):
    """Options for sorting /search results by a given field."""

    RELEVANCE = ""
    TITLE_ASC = "title:asc"
    TITLE_DESC = "title:desc"
    DATE_ASC = "date:asc"
    DATE_DESC = "date:desc"
