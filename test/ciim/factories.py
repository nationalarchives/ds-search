def create_record(
    template_details=None,
    iaid="C0000000",
    source="CAT",
):
    """
    Return a sample response for a record.
    Useful for tidying up tests where response needs to be mocked.
    otherwise creates a record with iaid
    """
    if not template_details:
        template_details = {"iaid": iaid, "source": source}

    # a typical record
    record = {"@template": {"details": template_details}}

    return record


def create_response(records=None):
    """
    Create a simple response for provided records.
    records: returns an empty data response or as given

    Ex:
    create_response(records=[]) # empty or no results
    create_response(records=[{<raw record>}, ])
    create_response(records=[create_record(),])
    create_response(records=[create_record(), create_record(iaid="C123456"), ])
    """

    if not records:
        records = []

    return {
        "data": records,
    }
