import responses
from app.lib.api import JSONAPIClient, ResourceNotFound
from app.records.models import Record
from app.search.api import search_records
from app.search.models import APISearchResponse
from django.conf import settings
from django.test import SimpleTestCase


class SearchRecordsTests(SimpleTestCase):
    def setUp(self):
        self.records_client = JSONAPIClient

    @responses.activate
    def test_search_records_response(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={
                "data": [{"@template": {"details": {"iaid": "C198022"}}}],
                "buckets": [
                    {
                        "name": "group",
                        "entries": [
                            {"value": "tna", "count": 1},
                        ],
                    }
                ],
                "stats": {
                    "total": 1,
                    "results": 1,
                },
            },
            status=200,
        )

        api_results = search_records(query="")

        self.assertIsInstance(api_results, APISearchResponse)
        self.assertIsInstance(api_results.records, list)
        self.assertEqual(len(api_results.records), 1)
        self.assertIsInstance(api_results.records[0], Record)
        self.assertEqual(api_results.stats_total, 1)
        self.assertEqual(api_results.stats_results, 1)
        self.assertEqual(api_results.buckets, {"tna": 1})

    @responses.activate
    def test_no_data_returned(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={},
            status=200,
        )

        with self.assertRaisesMessage(Exception, "No data returned"):
            _ = search_records(query="")

    @responses.activate
    def test_no_buckets_returned(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            json={
                "data": [{"@template": {"details": {"iaid": "C198022"}}}],
                "stats": {
                    "total": 1,
                    "results": 1,
                },
            },
            status=200,
        )

        with self.assertRaisesMessage(Exception, "No 'buckets' returned"):
            _ = search_records(query="")
