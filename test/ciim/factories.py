def create_record(
    template_details=None,
    iaid="C0000000",
):
    """
    Return a sample response for a record.
    Useful for tidying up tests where response needs to be mocked.
    template_details: KV details for the record when given,
    otherwise creates a record with iaid
    """
    if not template_details:
        template_details = {"iaid": iaid}

    # a typical record
    record = {"@template": {"details": template_details}}

    return record


def create_response(records=None):
    """
    Create a simple response for provided records.
    records: returns an empty data response or as given
    status_code: returns an error response when given

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
