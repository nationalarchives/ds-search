from app.lib.forms import BaseForm
from app.records.constants import TNA_LEVELS
from app.search.buckets import CATALOGUE_BUCKETS
from app.search.constants import Sort

from app.lib.fields import (
    CharField,
    ChoiceField,
    DynamicMultipleChoiceField,
)



class CatalogueSearchForm(BaseForm):

    def add_fields(self):

        return {
            "group": ChoiceField(
                choices=CATALOGUE_BUCKETS.as_choices(),
                validate_input=True,
            ),
            "sort": ChoiceField(
                choices=[
                    (Sort.RELEVANCE.value, "Relevance"),
                    (Sort.DATE_DESC.value, "Date (newest first)"),
                    (Sort.DATE_ASC.value, "Date (oldest first)"),
                    (Sort.TITLE_ASC.value, "Title (A–Z)"),
                    (Sort.TITLE_DESC.value, "Title (Z–A)"),
                ],
                validate_input=True,
            ),
            "q": CharField(),
            "level": DynamicMultipleChoiceField(
                label="Filter by levels",
                choices=tuple((level, level) for level in TNA_LEVELS.values()),
                validate_input=True,
            ),
        }
