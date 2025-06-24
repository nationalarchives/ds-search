from app.lib.fields import (
    CharField,
    ChoiceField,
    DynamicMultipleChoiceField,
)
from app.lib.forms import BaseForm
from app.records.constants import TNA_LEVELS
from app.search.buckets import CATALOGUE_BUCKETS
from app.search.constants import Sort

# TODO: Temporary replace as API queries by Lettercode, untill its updated to Deparment
TNA_LEVELS_BY_API = list(
    ("Lettercode", "Lettercode") if level == "Department" else (level, level)
    for level in TNA_LEVELS.values()
)


class CatalogueSearchForm(BaseForm):

    def add_fields(self):

        return {
            "group": ChoiceField(
                choices=CATALOGUE_BUCKETS.as_choices(),
            ),
            "sort": ChoiceField(
                choices=[
                    (Sort.RELEVANCE.value, "Relevance"),
                    (Sort.DATE_DESC.value, "Date (newest first)"),
                    (Sort.DATE_ASC.value, "Date (oldest first)"),
                    (Sort.TITLE_ASC.value, "Title (A–Z)"),
                    (Sort.TITLE_DESC.value, "Title (Z–A)"),
                ],
            ),
            "q": CharField(),
            "level": DynamicMultipleChoiceField(
                label="Filter by levels",
                choices=TNA_LEVELS_BY_API,
                validate_input=True,  # validate input with choices before querying the API
            ),
        }
