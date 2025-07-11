from app.lib.api import ResourceNotFound, rosetta_request_handler
from app.records.models import APIResponse, Record


def record_details_by_id(id, params={}) -> Record:
    """Fetches a record by its ID from the Rosetta API.
    The errors are handled by a custom middleware in the app."""
    uri = "get"
    params.update({"id": id})
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
