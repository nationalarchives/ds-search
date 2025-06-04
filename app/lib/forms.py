from typing import Any

from app.records.constants import TNA_LEVELS
from app.search.buckets import CATALOGUE_BUCKETS
from app.search.constants import Sort
from django.http import QueryDict

from .fields import (
    BaseField,
    ValidationError,
)


class BaseForm:

    def __init__(self, data=None) -> None:

        self.data = data or {}  # request data usually with defaults
        self.cleaned_data: dict[str, Any] = {}  # usually from request for API
        self._fields: dict[str, BaseField] = self.add_fields()
        self._errors = {}  # overall error form and fields
        # self.is_bound = bool(data)

        self.bind_fields()
        # binds the form data to the fields on initialise
        # if self.is_bound and self._fields:
        #     self.bind_fields()
        # else:
        #     raise ValidationError("Unbound fields with data")

    @property
    def fields(self):
        return self._fields

    def add_fields(self) -> dict[str, BaseField]:
        """Implement in SubClass. Ex {"<field_name>": <Field>, }"""
        return {}

    def _get_data_from_querydict(self, key, data):
        "Returns appropriate value from a QueryDict"
        values = data.getlist(key)
        if not values:
            return None
        if len(values) == 1:
            return values[0]
        return values

    def bind_fields(self):
        """Binds fields with data"""

        # if not self.is_bound:
        #     return

        for name, field in self.fields.items():
            value = self._get_data_from_querydict(name, self.data)
            field.bind(name, value)

    def is_valid(self):
        """Returns True when fields are cleaned and validated without errors and stores cleaned data.
        When False, adds overall errors for form and field"""
        valid = True

        # clean and validate fields
        for name, field in self.fields.items():
            if not field.is_valid():
                self.add_error(name, message=field.error.get("text"))
                valid = False
            else:
                self.cleaned_data[name] = field.get_cleaned_value()

        # clean and validate fields at form level
        if valid:
            try:
                self.cross_validate()
            except ValidationError as e:
                self.add_error(key="NONFIELDERROR", message={"text": str(e)})
                valid = False

        return valid

    def cross_validate(self):
        """Subclass to validate between fields in cleaned data and raise Validation Error"""

    def add_error(self, key, message):
        """Key would be field name, or non field"""
        self._errors[key] = {"text": message}

    @property
    def errors(self) -> dict:
        return self._errors


