from app.lib.api import ResourceNotFound, rosetta_request_handler, iiif_request_handler
from app.records.models import APIResponse, Record, IIIFManifest


def record_details_by_id(id, params={}) -> Record:
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


def iiif_manifest_by_id(id) -> IIIFManifest:
    results = iiif_request_handler(id)
    # Get all images from the manifest - for HTML-only version?
    for item in results.get("items", []):
        if "items" in item:
            print(item["items"][0]["items"][0]["body"]["id"])
    if len(results["data"]) == 1: # TODO: Check if this is the correct way to get a manifest when endpoint is created
        manifest_data = results["data"][0]
        response = APIResponse(manifest_data)
        return response.manifest
    raise ResourceNotFound(f"id {id} does not exist")
    