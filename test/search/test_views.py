import responses
from app.records.models import Record
from django.conf import settings
from django.test import TestCase


class CatalogueSearchViewTests(TestCase):

    @responses.activate
    def test_catalogue_search_view(self):

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
            status=200,
        )

        response = self.client.get("/catalogue/search/")

        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.context_data.get("results"), list)
        self.assertEqual(len(response.context_data.get("results")), 1)
        self.assertIsInstance(response.context_data.get("results")[0], Record)
        self.assertEqual(
            response.context_data.get("stats"),
            {"total": 26008838, "results": 20},
        )
        self.assertEqual(
            response.context_data.get("results_range"), {"from": 1, "to": 20}
        )
        self.assertEqual(response.context_data.get("selected_filters"), [])
        self.assertEqual(
            response.context_data.get("pagination"),
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
            response.context_data.get("buckets"),
            [
                {
                    "name": "Records at the National Archives (1)",
                    "href": "?group=tna",
                    "current": True,
                },
                {
                    "name": "Online records at The National Archives (0)",
                    "href": "?group=digitised",
                    "current": False,
                },
                {
                    "name": "Records at other UK archives (0)",
                    "href": "?group=nonTna",
                    "current": False,
                },
            ],
        )
