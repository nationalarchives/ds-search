import copy
import math
from typing import Any

from app.errors import views as errors_view
from app.lib.api import ResourceNotFound
from .forms import CatalogueSearchForm
from app.lib.pagination import pagination_object
from app.records.constants import CLOSURE_STATUSES, COLLECTIONS, TNA_LEVELS
from app.search.api import search_records
from config.jinja2 import qs_remove_value, qs_toggle_value
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from .api import APISearchResponse
from .buckets import CATALOGUE_BUCKETS, BucketKeys
from .constants import Sort


class CatalogueSearchView(TemplateView):

    template_name = "search/catalogue.html"
    default_group = BucketKeys.TNA.value
    default_sort = Sort.RELEVANCE.value  # sort includes ordering
    RESULTS_PER_PAGE = 20  # max records to show per page
    PAGE_LIMIT = 500  # max page number that can be queried

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:

        super().setup(request, *args, **kwargs)

        self.sort = self.request.GET.get("sort", self.default_sort)
        self.query = self.request.GET.get("q", "")

        self.bucket_list = copy.deepcopy(CATALOGUE_BUCKETS)
        self.current_bucket_key = (
            self.request.GET.get("group") or self.default_group
        )
        self.current_bucket = self.bucket_list.get_bucket(self.current_bucket_key)

        self.form = CatalogueSearchForm(**self.get_form_kwargs())


        self.api_result = None
        # self.current_bucket_key = self.form.cleaned_data.get("group")
        # if self.current_bucket_key and getattr(self, "bucket_list", None):
        #     self.current_bucket = self.bucket_list.get_bucket(self.current_bucket_key)

    def get_defaults(self):

        return {
            "group": self.default_group,
            "sort": self.default_sort,
        }

    def get_form_kwargs(self) -> dict[str, Any]:
        """Returns request data with default values if not given"""

        kwargs = {}
        data = self.request.GET.copy()

        # remove param with empty string values to properly set default values ex group v/s required settings
        for key in list(data.keys()):
            if all(value == "" for value in data.getlist(key)):
                del data[key]

        # Add any default values
        for k, v in self.get_defaults().items():
            data.setdefault(k, v)

        kwargs["data"] = data
        return kwargs

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Overrrides TemplateView.get() to process the form
        and continue with form_valid() or form_invalid() as appropriate.
        """

        if self.form.is_valid():
            return self.form_valid()
        return self.form_invalid()

    def form_valid(self) -> HttpResponse:
        self.process_valid_form(form=self.form)
        context = self.get_context_data(form=self.form)
        return self.render_to_response(context)

    def form_invalid(self):
        context = {
            "form": self.form,
            "results": {},
            "bucket_items": [],
            "results_range": [],
            "stats": {},
            "bucket_list": self.bucket_list,
            "bucket_keys": BucketKeys,
            "errors": self.form.errors,
            "level": self.form.fields["level"],
            "closure_statuses": CLOSURE_STATUSES,
            "collections": COLLECTIONS,
            "selected_filters": {},
        }
        return self.render_to_response(context=context)

    def process_valid_form(self, form):
        self.api_result = self.get_api_result()
        self.process_api_result()

    def process_api_result(self):
        pass

    def get_context_data(self, **kwargs):
        context: dict = super().get_context_data(**kwargs)
        context.update(
            {
                "level": self.form.fields["level"],
                "closure_statuses": CLOSURE_STATUSES,
                "collections": COLLECTIONS,
            }
        )

        results_range, pagination = self.paginate_api_result()

        selected_filters = build_selected_filters_list(self.request)

        self.bucket_list.update_buckets_for_display(
            query=self.query,
            buckets=self.api_result.buckets,
            current_bucket_key=self.current_bucket_key,
        )

        context.update(
            {
                "results": self.api_result.records,
                "bucket_list": self.bucket_list,
                "results_range": results_range,
                "stats": {
                    "total": self.api_result.stats_total,
                    "results": self.api_result.stats_results,
                },
                "selected_filters": selected_filters,
                "pagination": pagination,
                "bucket_keys": BucketKeys,
            }
        )
        return context

    def get_api_params(self) -> dict:

        params = {}

        # filter records for a bucket
        params.update({"filter": f"group:{self.current_bucket_key}"})

        # aggregations
        params.update({"aggs": self.current_bucket.aggregations})

        return params

    def get_api_result(self) -> APISearchResponse:

        try:
            return search_records(
                query=self.query,
                results_per_page=self.RESULTS_PER_PAGE,
                page=self.page,
                sort=self.sort,
                params=self.get_api_params(),
            )
        except ResourceNotFound:
            context = {
                "form": self.form,
                "bucket_list": [{}],
                "bucket_keys": {},
            }
            return TemplateResponse(
                request=self.request,
                template=self.template_name,
                context=context,
            )

    @property
    def page(self) -> int | HttpResponse:
        try:
            page = int(self.request.GET.get("page", 1))
            if page < 1:
                raise ValueError
        except (ValueError, KeyError):
            return errors_view.page_not_found_error_view(request=self.request)
        return page

    def paginate_api_result(self) -> tuple | HttpResponse:

        pages = math.ceil(self.api_result.stats_total / self.RESULTS_PER_PAGE)
        if pages > self.PAGE_LIMIT:
            pages = self.PAGE_LIMIT

        if self.page > pages:
            return errors_view.page_not_found_error_view(request=self.request)

        results_range = {
            "from": ((self.page - 1) * self.RESULTS_PER_PAGE) + 1,
            "to": ((self.page - 1) * self.RESULTS_PER_PAGE)
            + self.api_result.stats_results,
        }

        pagination = pagination_object(self.page, pages, self.request.GET)

        return (results_range, pagination)


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
        levels_lookup = {}
        for _, v in TNA_LEVELS.items():
            levels_lookup.update({v:v})

        for level in levels:
            selected_filters.append(
                {
                    # "label": f"Level: {TNA_LEVELS.get(level)}",
                    "label": f"Level: {levels_lookup.get(level)}",
                    "href": f"?{qs_toggle_value(request.GET, 'level', level)}",
                    # "title": f"Remove {TNA_LEVELS.get(level)} level",
                    "title": f"Remove {levels_lookup.get(level)} level",
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
