from app.lib.api import JSONAPIClient, ResourceNotFound
from app.records.models import APIResponse
from django.conf import settings


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
    if "data" not in results:
        raise Exception(f"No data returned for IAID {iaid}")
    if len(results["data"]) > 1:
        raise Exception(f"Multiple records returned for IAID {iaid}")
    if record_data := results["data"][0]:
        response = APIResponse(record_data)
        return response.record
    raise ResourceNotFound(f"IAID {iaid} does not exist")


def record_details_by_ref(reference, params={}):
    # TODO
    pass


def search_records(query, params={}):
    uri = "search"
    params = params | {
        "q": query,
    }
    results = rosetta_request_handler(uri, params)
    if "data" not in results:
        raise Exception("No data returned")
    if not len(results["data"]):
        raise ResourceNotFound("No results found")
    return [APIResponse(record_data).record for record_data in results["data"]]
