def validate_setting(obj, attr_name, expected_type, default=None):
    """
    Checks if an attribute exists on an object, and validates its type.

    Args:
        obj: The object to check for the attribute (e.g., settings)
        attr_name: The name of the attribute to check (e.g., 'DELIVERY_OPTIONS_DCS_LIST')
        expected_type: The type to validate against (e.g., str, int, list)
        default: The default value to return if validation fails

    Returns:
        The attribute value if it exists and is of the expected type, otherwise the default

    Example Usage:
        dcs = validate_setting(settings, 'DELIVERY_OPTIONS_DCS_LIST', str, default="")
        # dcs will be the string value if it exists, or an empty string if not

        # You can also use it with other types
        max_retries = validate_setting(settings, 'MAX_RETRIES', int, default=3)
        allowed_hosts = validate_setting(settings, 'ALLOWED_HOSTS', list, default=[])
    """
    value = getattr(obj, attr_name, None)
    return (
        value
        if value is not None and isinstance(value, expected_type)
        else default
    )
