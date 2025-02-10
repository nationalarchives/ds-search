from app.lib.api import JSONAPIClient, ResourceNotFound
from app.records.models import APIResponse, APISearchResponse
from django.conf import settings


def rosetta_request_handler(uri, params={}):
    api_url = settings.ROSETTA_API_URL
    if not api_url:
        raise Exception("ROSETTA_API_URL not set")
    client = JSONAPIClient(api_url)
    client.add_parameters(params)
    data = client.get(uri)
    return data


def record_details_by_id(id, params={}):
    uri = "get"
    params = params | {
        "id": id,
    }
    results = rosetta_request_handler(uri, params)
    if "data" not in results:
        raise Exception(f"No data returned for id {id}")
    if len(results["data"]) > 1:
        raise Exception(f"Multiple records returned for id {id}")
    if record_data := results["data"][0]:
        response = APIResponse(record_data)
        return response.record
    raise ResourceNotFound(f"id {id} does not exist")


def record_details_by_ref(reference, params={}):
    # TODO: Implement record_details_by_ref once Rosetta has support
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
    return APISearchResponse(results)
