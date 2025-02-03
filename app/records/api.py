from app.lib.api import JSONAPIClient, ResourceNotFound
from app.records.models import Record
from django.conf import settings
from pydash import objects


def rosetta_request_handler(uri, params={}):
    api_url = settings.ROSETTA_API_URL
    if not api_url:
        raise Exception("ROSETTA_API_URL not set")
    client = JSONAPIClient(api_url)
    client.add_parameters(params)
    data = client.get(uri)
    return data


def record_details_by_iaid(iaid, params={}):
    uri = "get"
    params = params | {
        "id": iaid,
    }
    results = rosetta_request_handler(uri, params)
    if len(objects.get(results, "data", [])) > 1:
        raise Exception(f"Multiple records returned for IAID {iaid}")
    record_data = objects.get(results, "data[0]", [])
    if not record_data:
        raise ResourceNotFound(f"IAID {iaid} does not exist")
    return Record(record_data)


def record_details_by_ref(reference, params={}):
    # TODO
    pass
