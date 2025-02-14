from django.urls.converters import StringConverter


class IDConverter(StringConverter):
    """Converter used to extract id's from a URL."""

    regex = r"([ACDFN][0-9]{1,8}|[a-f0-9]{8}-?([a-f0-9]{4}-?){3}[a-f0-9]{12}(_[1-9])?)"
