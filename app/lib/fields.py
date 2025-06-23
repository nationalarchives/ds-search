"""Module for custom fields which interfaces with FE component attrs."""


class ValidationError(Exception):
    pass


class BaseField:
    """
    Flow
    -----
    1. Instantiate the field
    2. Bind the request value
    3. Clean and Validate the value. Assign clean value.
    4. Assign error on failure
    5. Access field attributes
    """

    def __init__(self, label=None, required=False, hint=""):
        self.label = label
        self.required = required
        self.hint = hint
        self._value = None  # usually the request data
        self._error = {}
        self.choices = None  # applicable to certain fields ex choice

    def bind(self, name, value: list | str) -> None:
        """Binds field name, value to the field. The value is usually from
        user input. Binding happens through the form on initialisation.
        Override to bind to list or string."""

        self.name = name
        self.label = self.label or name.capitalize()
        self._value = value

    def is_valid(self):
        """Runs cleaning and validation. Handles ValidationError.
        Stores cleaned value. Returns True if valid, False otherwise"""

        try:
            self._cleaned = self.clean(self.value)
        except ValidationError as e:
            self.add_error(str(e))

        return not self._error

    def clean(self, value):
        """Subclass for cleaning and validating. Ex strip str, convert to date object"""

        self.validate(value)
        return value

    def validate(self, value):
        """Basic validation. For more validation, Subclass and raise ValidationError"""

        if self.required and not value:
            raise ValidationError("Value is required.")

    def add_error(self, message):
        """Stores error message in the format of FE component"""

        self._error = {"text": message}

    @property
    def error(self) -> dict[str, str]:
        return self._error

    @property
    def cleaned(self):
        return self._cleaned if not self._error else None

    @property
    def value(self):
        return self._value

    @property
    def update_choices(self):
        """Inplement for multiple choice fields"""

        raise NotImplementedError

    @property
    def items(self):
        """Return as required by FE.
        Ex Checkboxes [{"text": "Alpha","value": "alpha"},{"text": "Beta","value": "beta","checked": true}]
        """

        raise NotImplementedError


class CharField(BaseField):

    def bind(self, name, value: list | str) -> None:
        """Binds a empty string or last value from input."""

        if not value:
            value = [""]
        # get last value (for more than one input value)
        value = value[-1]
        super().bind(name, value)

    def clean(self, value):
        value = super().clean(value)
        return str(value).strip() if value else ""


class ChoiceField(BaseField):

    def __init__(self, choices: list[tuple[str, str]], **kwargs):
        """choices: format [(field value, display value),]."""

        super().__init__(**kwargs)
        self.choices = choices

    def _has_match(self, value, search_in):
        return value in search_in

    def bind(self, name, value: list | str) -> None:
        """Binds a empty string or last value from input."""

        if not value:
            value = [""]
        # get last value (for more than one input value)
        value = value[-1]
        super().bind(name, value)

    def validate(self, value):
        if self.required:
            super().validate(value)

        valid_choices = [value for value, _ in self.choices]
        if not self._has_match(value, valid_choices):
            raise ValidationError(
                (
                    f"Enter a valid choice. [{value or 'Empty param value'}] is not one of the available choices. "
                    f"Valid choices are [{', '.join(valid_choices)}]"
                )
            )

    @property
    def items(self):
        return [
            (
                {"text": display_value, "value": value, "checked": True}
                if (value == self.value)
                else {"text": display_value, "value": value}
            )
            for value, display_value in self.choices
        ]


class DynamicMultipleChoiceField(BaseField):

    def __init__(self, choices: list[tuple[str, str]], **kwargs):
        """choices: format [(field value, display value),]. Has field specific attributes."""

        # field specific attr, validate input choices before querying the api
        self.validate_input = bool(choices) and kwargs.pop(
            "validate_input", True
        )
        super().__init__(**kwargs)
        self.choices = choices

    def _has_match_all(self, value, search_in):
        return all(item in search_in for item in value)

    def validate(self, value):
        if self.required or self.validate_input:
            super().validate(value)
            if self.validate_input:
                valid_choices = [value for value, _ in self.choices]
                if not self._has_match_all(value, valid_choices):
                    raise ValidationError(
                        (
                            f"Enter a valid choice. Value(s) [{', '.join(value)}] do not belong "
                            f"to the available choices. Valid choices are [{', '.join(valid_choices)}]"
                        )
                    )

    @property
    def items(self):
        return [
            (
                {"text": display_value, "value": value, "checked": True}
                if (value in self.value)
                else {"text": display_value, "value": value}
            )
            for value, display_value in self.choices
        ]
