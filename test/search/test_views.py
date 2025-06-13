from http import HTTPStatus

import responses
from app.records.models import Record
from app.search.buckets import BucketKeys
from app.search.forms import CatalogueSearchForm
from django.conf import settings
from django.test import TestCase


class CatalogueSearchViewTests(TestCase):

    @responses.activate
    def test_catalogue_search_context_without_params(self):

        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={
                "data": [
                    {
                        "@template": {
                            "details": {
                                "iaid": "C123456",
                                "source": "CAT",
                            }
                        }
                    }
                ],
                "buckets": [
                    {
                        "name": "group",
                        "entries": [
                            {"value": "tna", "count": 1},
                        ],
                    }
                ],
                "stats": {
                    "total": 26008838,
                    "results": 20,
                },
            },
            status=HTTPStatus.OK,
        )

        self.response = self.client.get("/catalogue/search/")
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

        self.assertIsInstance(self.response.context_data.get("results"), list)
        self.assertEqual(len(self.response.context_data.get("results")), 1)
        self.assertIsInstance(
            self.response.context_data.get("results")[0], Record
        )
        self.assertEqual(
            self.response.context_data.get("stats"),
            {"total": 26008838, "results": 20},
        )

        self.assertEqual(
            self.response.context_data.get("results_range"),
            {"from": 1, "to": 20},
        )

        self.assertEqual(self.response.context_data.get("selected_filters"), [])

        self.assertEqual(
            self.response.context_data.get("pagination"),
            {
                "items": [
                    {"number": "1", "href": "?page=1", "current": True},
                    {"number": "2", "href": "?page=2", "current": False},
                    {"ellipsis": True},
                    {"number": "500", "href": "?page=500", "current": False},
                ],
                "next": {"href": "?page=2", "title": "Next page of results"},
            },
        )

        self.assertEqual(
            self.response.context_data.get("bucket_list").items,
            [
                {
                    "name": "Records at the National Archives (1)",
                    "href": "?group=tna",
                    "current": True,
                },
                {
                    "name": "Records at other UK archives (0)",
                    "href": "?group=nonTna",
                    "current": False,
                },
            ],
        )
        self.assertEqual(
            self.response.context_data.get("bucket_keys"), BucketKeys
        )

        # ### form ###
        self.assertIsInstance(
            self.response.context_data.get("form"), CatalogueSearchForm
        )
        self.assertEqual(self.response.context_data.get("form").errors, {})
        self.assertEqual(
            self.response.context_data.get("form").cleaned_data,
            {"group": "tna", "sort": "", "q": "", "level": []},
        )
        self.assertEqual(len(self.response.context_data.get("form").fields), 4)

        # ### form fields ###

        self.assertEqual(
            self.response.context_data.get("form").fields["q"].name, "q"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["q"].value, ""
        )

        self.assertEqual(
            self.response.context_data.get("form").fields["group"].name, "group"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["group"].value, "tna"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["group"].items,
            [
                {
                    "text": "Records at the National Archives",
                    "value": "tna",
                    "checked": True,
                },
                {"text": "Records at other UK archives", "value": "nonTna"},
            ],
        )

        self.assertEqual(
            self.response.context_data.get("form").fields["sort"].name, "sort"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["sort"].value, ""
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["sort"].items,
            [
                {"text": "Relevance", "value": "", "checked": True},
                {"text": "Date (newest first)", "value": "date:desc"},
                {"text": "Date (oldest first)", "value": "date:asc"},
                {"text": "Title (A–Z)", "value": "title:asc"},
                {"text": "Title (Z–A)", "value": "title:desc"},
            ],
        )

        self.assertEqual(
            self.response.context_data.get("form").fields["level"].name, "level"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["level"].label,
            "Filter by levels",
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["level"].value, []
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["level"].items,
            [
                {"text": "Department", "value": "Department"},
                {"text": "Division", "value": "Division"},
                {"text": "Series", "value": "Series"},
                {"text": "Sub-series", "value": "Sub-series"},
                {"text": "Sub-sub-series", "value": "Sub-sub-series"},
                {"text": "Piece", "value": "Piece"},
                {"text": "Item", "value": "Item"},
            ],
        )

    @responses.activate
    def test_catalogue_search_context_with_query_param(self):

        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={
                "data": [
                    {
                        "@template": {
                            "details": {
                                "iaid": "C123456",
                                "source": "CAT",
                            }
                        }
                    }
                ],
                "buckets": [
                    {
                        "name": "group",
                        "entries": [
                            {"value": "tna", "count": 1},
                        ],
                    }
                ],
                "stats": {
                    "total": 26008838,
                    "results": 20,
                },
            },
            status=HTTPStatus.OK,
        )

        self.response = self.client.get("/catalogue/search/?q=ufo")
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(
            self.response.context_data.get("form").fields["q"].name, "q"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["q"].value,
            "ufo",
        )

    @responses.activate
    def test_catalogue_search_context_with_sort_param(self):

        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={
                "data": [
                    {
                        "@template": {
                            "details": {
                                "iaid": "C123456",
                                "source": "CAT",
                            }
                        }
                    }
                ],
                "buckets": [
                    {
                        "name": "group",
                        "entries": [
                            {"value": "tna", "count": 1},
                        ],
                    }
                ],
                "stats": {
                    "total": 26008838,
                    "results": 20,
                },
            },
            status=HTTPStatus.OK,
        )

        self.response = self.client.get("/catalogue/search/?sort=title:asc")
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(
            self.response.context_data.get("form").fields["sort"].name, "sort"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["sort"].value,
            "title:asc",
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["sort"].items,
            [
                {
                    "text": "Relevance",
                    "value": "",
                },
                {
                    "text": "Date (newest first)",
                    "value": "date:desc",
                },
                {"text": "Date (oldest first)", "value": "date:asc"},
                {"text": "Title (A–Z)", "value": "title:asc", "checked": True},
                {"text": "Title (Z–A)", "value": "title:desc"},
            ],
        )

    @responses.activate
    def test_catalogue_search_context_with_group_param(self):

        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={
                "data": [
                    {
                        "@template": {
                            "details": {
                                "iaid": "C123456",
                                "source": "CAT",
                            }
                        }
                    }
                ],
                "buckets": [
                    {
                        "name": "group",
                        "entries": [
                            {"value": "nonTna", "count": 1},
                        ],
                    }
                ],
                "stats": {
                    "total": 26008838,
                    "results": 20,
                },
            },
            status=HTTPStatus.OK,
        )

        self.response = self.client.get("/catalogue/search/?group=nonTna")
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(
            self.response.context_data.get("form").fields["group"].name, "group"
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["group"].value,
            "nonTna",
        )

        self.assertEqual(
            self.response.context_data.get("form").fields["group"].items,
            [
                {
                    "text": "Records at the National Archives",
                    "value": "tna",
                },
                {
                    "text": "Records at other UK archives",
                    "value": "nonTna",
                    "checked": True,
                },
            ],
        )

    @responses.activate
    def test_catalogue_search_context_with_level_param(self):

        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={
                "data": [
                    {
                        "@template": {
                            "details": {
                                "iaid": "C123456",
                                "source": "CAT",
                            }
                        }
                    }
                ],
                "buckets": [
                    {
                        "name": "group",
                        "entries": [
                            {"value": "nonTna", "count": 1},
                        ],
                    }
                ],
                "stats": {
                    "total": 26008838,
                    "results": 20,
                },
            },
            status=HTTPStatus.OK,
        )

        self.response = self.client.get(
            "/catalogue/search/?level=Item&level=Division"
        )

        self.assertEqual(
            self.response.context_data.get("form").fields["level"].value,
            ["Item", "Division"],
        )
        self.assertEqual(
            self.response.context_data.get("form").fields["level"].items,
            [
                {"text": "Department", "value": "Department"},
                {"text": "Division", "value": "Division", "checked": True},
                {"text": "Series", "value": "Series"},
                {"text": "Sub-series", "value": "Sub-series"},
                {"text": "Sub-sub-series", "value": "Sub-sub-series"},
                {"text": "Piece", "value": "Piece"},
                {"text": "Item", "value": "Item", "checked": True},
            ],
        )
