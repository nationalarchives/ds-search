from app.lib.api import ResourceNotFound, rosetta_request_handler
from app.records.models import APISearchResponse


def search_records(query, params={}) -> APISearchResponse:
    uri = "search"
    params.update({"q": query})
    results = rosetta_request_handler(uri, params)
    if "data" not in results:
        raise Exception("No data returned")
    if not len(results["data"]):
        raise ResourceNotFound("No results found")
    return APISearchResponse(results)
