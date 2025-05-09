import math

from app.errors import views as errors_view
from app.lib.api import ResourceNotFound
from app.lib.pagination import pagination_object
from app.records.constants import TNA_LEVELS
from app.search.api import search_records
from config.jinja2 import qs_remove_value, qs_toggle_value
from django.template.response import TemplateResponse

from .buckets import BucketKeys, get_buckets_for_display


def catalogue_search_view(request):
    template = "search/catalogue.html"
    context: dict = {
        "levels": TNA_LEVELS,
    }
    results_per_page = 20
    page = int(request.GET.get("page", 1))
    sort_order = request.GET.get("sort", "").split(":")
    sort = sort_order[0] if sort_order else ""
    order = sort_order[1] if len(sort_order) > 1 else ""

    current_bucket_key = request.GET.get("group", BucketKeys.TNA)
    # filter records for a bucket
    params = {"filter": f"group:{current_bucket_key}"}

    query = request.GET.get("q", "")

    try:
        results = search_records(
            query=query,
            results_per_page=results_per_page,
            page=page,
            sort=sort,
            order=order,
            params=params,
        )
    except ResourceNotFound:
        return TemplateResponse(
            request=request,
            template=template,
            context=context,
        )

    pages = math.ceil(results.stats_total / results_per_page)
    if pages > 500:
        pages = 500
    if page > pages:
        return errors_view.page_not_found_error_view(request=request)
    results_range = {
        "from": ((page - 1) * results_per_page) + 1,
        "to": ((page - 1) * results_per_page) + results.stats_results,
    }
    selected_filters = build_selected_filters_list(request)
    buckets = get_buckets_for_display(
        query=query,
        buckets=results.buckets,
        current_bucket_key=current_bucket_key,
    )

    context.update(
        {
            "results": results.records,
            "buckets": buckets,
            "results_range": results_range,
            "stats": {
                "total": results.stats_total,
                "results": results.stats_results,
            },
            "selected_filters": selected_filters,
            "pagination": pagination_object(page, pages, request.GET),
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
    return selected_filters
