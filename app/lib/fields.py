"""Module for custom fields which interfaces with FE component attrs."""


class ValidationError(Exception):
    pass


class BaseField:

    def __init__(self, label=None, required=False, hint=""):
        self.label = label
        self.required = required
        self.hint = hint
        self._value = None  # usually the request data
        self._error = {}
        self.choices = None

    def bind(self, name, value) -> None:
        """Binds field name, value to the field. The value is usually from
        user input. Binding happens through the form on initialisation."""

        self.name = name
        self.label = self.label or name.capitalize()
        self._value = value

    def clean(self, value):
        """Subclass for cleaning and validating. Ex convert to date object"""

        self.validate(value)
        return value

    def validate(self, value):
        """Basic validation. For more validation, Subclass and raise ValidationError"""

        if self.required and not value:
            raise ValidationError("Value is required.")

    def is_valid(self):
        """Runs cleaning and validation. Handles ValidationError.
        Stores cleaned value. Returns True if valid, False otherwise"""

        try:
            self._cleaned = self.clean(self.value)
        except ValidationError as e:
            self.add_error(str(e))

        return not self._error

    def add_error(self, message):
        """Stores error message in the format of FE component"""

        self._error = {"text": message}

    @property
    def error(self):
        return self._error

    def get_cleaned_value(self):
        return self._cleaned if not self._error else None

    @property
    def value(self):
        return self._value

    @property
    def update_choices(self):
        """For choice fields"""

        raise NotImplementedError

    @property
    def items(self):
        """Return as required by FE.
        Ex Checkboxes [{"text": "Alpha","value": "alpha"},{"text": "Beta","value": "beta","checked": true}]
        """

        raise NotImplementedError


class CharField(BaseField):

    def bind(self, name, value):
        if not value:
            value = ""
        super().bind(name, value)

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, str):
            raise ValidationError(
                f"{self.label} must be a string. Given value is {value} is invalid."
            )


class ChoiceField(BaseField):

    def __init__(self, choices: list[tuple[str, str]], **kwargs):
        """choices: format [(field value, display value),]. Has field specific attributes."""

        # field specific attr
        self.validate_input = bool(choices) and kwargs.pop(
            "validate_input", True
        )
        super().__init__(**kwargs)
        self.choices = choices

    def _has_all_match(self, value, search_in):
        if isinstance(value, str):
            return value in search_in
        return all(item in search_in for item in value)

    def validate(self, value):
        super().validate(value)
        if self.validate_input and value:
            valid_choices = [value for value, _ in self.choices]
            if not self._has_all_match(value, valid_choices):
                raise ValidationError(
                    f"Enter a valid choice. {value} is not one of the available choices. Valid choices {', '.join(valid_choices)}"
                )

    @property
    def items(self):
        return [
            (
                {"text": display_value, "value": value, "checked": True}
                if self.value and self._has_all_match(value, self.value)
                else {"text": display_value, "value": value}
            )
            for value, display_value in self.choices
        ]

    @property
    def items_iter(self):
        for item in self.items:
            yield (item["value"], item["text"])


class DynamicMultipleChoiceField(ChoiceField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
