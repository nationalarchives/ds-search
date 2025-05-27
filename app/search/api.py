from app.lib.api import ResourceNotFound, rosetta_request_handler

from .models import APISearchResponse


def search_records(
    query, results_per_page=12, page=1, sort="", params={}
) -> APISearchResponse:
    uri = "search"
    params.update(
        {
            "q": query or "*",
            "size": results_per_page,
            "from": (page - 1) * results_per_page,
            "sort": sort,
        }
    )
    # remove params having no values
    params = {param: value for param, value in params.items() if value}
    results = rosetta_request_handler(uri, params)
    if "data" not in results:
        raise Exception("No data returned")
    if "buckets" not in results:
        raise Exception("No 'buckets' returned")
    if not len(results["data"]) and page == 1:
        raise ResourceNotFound("No results found")
    return APISearchResponse(results)
