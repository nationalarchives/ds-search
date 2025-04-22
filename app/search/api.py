from app.lib.api import ResourceNotFound, rosetta_request_handler

from .models import APISearchResponse


def search_records(
    query, results_per_page=12, page=1, sort="", order="asc", params={}
) -> APISearchResponse:
    uri = "search"
    params.update(
        {
            "q": query or "*",
            "size": results_per_page,
            "from": (page - 1) * results_per_page,
            "sort": sort,
            "sortOrder": order,
        }
    )
    results = rosetta_request_handler(uri, params)
    if "data" not in results:
        raise Exception("No data returned")
    if not len(results["data"]) and page == 1:
        raise ResourceNotFound("No results found")
    return APISearchResponse(results)
