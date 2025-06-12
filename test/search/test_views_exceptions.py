from http import HTTPStatus

import responses
from django.conf import settings
from django.test import TestCase, override_settings


class TestCatalogueSearchViewExceptions(TestCase):

    @override_settings(
        ROSETTA_API_URL="",
    )
    @responses.activate
    def test_missing_config_with_server_error(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/search",
            status=HTTPStatus.OK,
        )

        with self.assertLogs("app.search.views", level="ERROR") as lc:
            response = self.client.get("/catalogue/search/")

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn(
            "ERROR:app.search.views:ROSETTA_API_URL not set", lc.output
        )
