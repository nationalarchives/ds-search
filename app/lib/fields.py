class ValidationError(Exception):
    pass


class BaseField:

    def __init__(self, name, label=None, required=False, hint=""):
        self.name = name
        self.label = label or name.capitalize()
        self.required = required
        self.hint = hint
        self.value = None
        self.error = ""

    def clean(self, value):
        """Hook to clean and validate value. raise ValidationError accordingly"""
        self.validate(value)
        return value

    def validate(self, value):
        """Hook to validate value, raise ValidationError accordingly"""
        pass

    def bind(self, value):
        """Binds the value to the field, adds error for ValidationError"""
        try:
            self.value = self.clean(value)
        except ValidationError as e:
            self.add_error(str(e))

    def add_error(self, message):
        self.error = message

    @property
    def items(self):
        """Return as required by FE.
        Ex Checkboxes [{"text": "Alpha","value": "alpha"},{"text": "Beta","value": "beta","checked": true}]
        """
        raise NotImplementedError


class CharField(BaseField):

    def clean(self, value):
        value = super().clean(value)
        if not isinstance(value, str):
            raise ValidationError(
                f"{self.label} must be a string. Given value is {value} is invalid."
            )
        return value

    def bind(self, value):
        if not value:
            value = ""
        super().bind(value)


class ChoiceField(BaseField):

    def __init__(self, choices: list[tuple[str, str]], **kwargs):
        """choices: format [(field value, display value),]"""
        super().__init__(**kwargs)
        self.choices = choices

    def clean(self, value):
        value = super().clean(value)

        if self.required and not value:
            raise ValidationError(
                "At least one selection of the choice is required."
            )

        valid_choices = [value for value, _ in self.choices]
        if value not in valid_choices:
            raise ValidationError(
                f"Enter a valid choice. {value} is not one of the available choices."
            )

        return value

    @property
    def items(self):
        return [
            {"text": display_value, "value": value}
            for value, display_value in self.choices
        ]
