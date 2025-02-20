from app.lib.api import ResourceNotFound, rosetta_request_handler
from app.records.models import APIResponse, APISearchResponse, Record
from django.conf import settings


def record_details_by_id(id, params={}) -> Record:
    uri = "get"
    params = params | {
        "id": id,
    }
    results = rosetta_request_handler(uri, params)
    if "data" not in results:
        raise Exception(f"No data returned for id {id}")
    if len(results["data"]) > 1:
        raise Exception(f"Multiple records returned for id {id}")
    if len(results["data"]) == 1:
        record_data = results["data"][0]
        response = APIResponse(record_data)
        return response.record
    raise ResourceNotFound(f"id {id} does not exist")


def record_details_by_ref(reference, params={}):
    # TODO: Implement record_details_by_ref once Rosetta has support
    pass


def search_records(query, params={}) -> APISearchResponse:
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
