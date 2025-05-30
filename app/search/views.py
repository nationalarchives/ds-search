import copy
import math

from app.errors import views as errors_view
from app.lib.api import ResourceNotFound
from app.lib.pagination import pagination_object
from app.records.constants import CLOSURE_STATUSES, COLLECTIONS, TNA_LEVELS
from app.search.api import search_records
from config.jinja2 import qs_remove_value, qs_toggle_value
from django.template.response import TemplateResponse

from .buckets import CATALOGUE_BUCKETS, BucketKeys
from .constants import Sort


def catalogue_search_view(request):
    template = "search/catalogue.html"
    bucket_list = copy.deepcopy(CATALOGUE_BUCKETS)
    default_group = BucketKeys.TNA.value
    default_sort = Sort.RELEVANCE.value  # sort includes ordering
    RESULTS_PER_PAGE = 20  # max records to show per page
    PAGE_LIMIT = 500  # max page number that can be queried

    context: dict = {
        "levels": TNA_LEVELS,
        "closure_statuses": CLOSURE_STATUSES,
        "collections": COLLECTIONS,
    }

    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            raise ValueError
    except (ValueError, KeyError):
        return errors_view.page_not_found_error_view(request=request)

    sort = request.GET.get("sort", default_sort)
    current_bucket_key = request.GET.get("group") or default_group
    query = request.GET.get("q", "")

    # filter records for a bucket
    params = {"filter": f"group:{current_bucket_key}"}

    try:
        results = search_records(
            query=query,
            results_per_page=RESULTS_PER_PAGE,
            page=page,
            sort=sort,
            params=params,
        )
    except ResourceNotFound:
        context.update({"bucket_list": [{}], "bucket_keys": {}})
        return TemplateResponse(
            request=request,
            template=template,
            context=context,
        )

    pages = math.ceil(results.stats_total / RESULTS_PER_PAGE)
    if pages > PAGE_LIMIT:
        pages = PAGE_LIMIT
    if page > pages:
        return errors_view.page_not_found_error_view(request=request)
    results_range = {
        "from": ((page - 1) * RESULTS_PER_PAGE) + 1,
        "to": ((page - 1) * RESULTS_PER_PAGE) + results.stats_results,
    }
    selected_filters = build_selected_filters_list(request)
    bucket_list.update_buckets_for_display(
        query=query,
        buckets=results.buckets,
        current_bucket_key=current_bucket_key,
    )

    context.update(
        {
            "results": results.records,
            "bucket_list": bucket_list,
            "results_range": results_range,
            "stats": {
                "total": results.stats_total,
                "results": results.stats_results,
            },
            "selected_filters": selected_filters,
            "pagination": pagination_object(page, pages, request.GET),
            "bucket_keys": BucketKeys,
        }
    )
    return TemplateResponse(request=request, template=template, context=context)


def build_selected_filters_list(request):
    selected_filters = []
    # if request.GET.get("q", None):
    #     selected_filters.append(
    #         {
    #             "label": f"\"{request.GET.get('q')}\"",
    #             "href": f"?{qs_remove_value(request.GET, 'q')}",
    #             "title": f"Remove query: \"{request.GET.get('q')}\"",
    #         }
    #     )
    if request.GET.get("search_within", None):
        selected_filters.append(
            {
                "label": f'Sub query "{request.GET.get("search_within")}"',
                "href": f"?{qs_remove_value(request.GET, 'search_within')}",
                "title": "Remove search within",
            }
        )
    if request.GET.get("date_from", None):
        selected_filters.append(
            {
                "label": f"Record date from: {request.GET.get("date_from")}",
                "href": f"?{qs_remove_value(request.GET, 'date_from')}",
                "title": "Remove record from date",
            }
        )
    if request.GET.get("date_to", None):
        selected_filters.append(
            {
                "label": f"Record date to: {request.GET.get("date_to")}",
                "href": f"?{qs_remove_value(request.GET, 'date_to')}",
                "title": "Remove record to date",
            }
        )
    if levels := request.GET.getlist("level", None):
        for level in levels:
            selected_filters.append(
                {
                    "label": f"Level: {TNA_LEVELS.get(level)}",
                    "href": f"?{qs_toggle_value(request.GET, 'level', level)}",
                    "title": f"Remove {TNA_LEVELS.get(level)} level",
                }
            )
    if closure_statuses := request.GET.getlist("closure_status", None):
        for closure_status in closure_statuses:
            selected_filters.append(
                {
                    "label": f"Closure status: {CLOSURE_STATUSES.get(closure_status)}",
                    "href": f"?{qs_toggle_value(request.GET, 'closure_status', closure_status)}",
                    "title": f"Remove {CLOSURE_STATUSES.get(closure_status)} closure status",
                }
            )
    if collections := request.GET.getlist("collections", None):
        for collection in collections:
            selected_filters.append(
                {
                    "label": f"Collection: {COLLECTIONS.get(collection)}",
                    "href": f"?{qs_toggle_value(request.GET, 'collections', collection)}",
                    "title": f"Remove {COLLECTIONS.get(collection)} collection",
                }
            )
    return selected_filters
