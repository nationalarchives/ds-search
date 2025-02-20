from test.utils import prevent_request_warnings

import responses
from django.conf import settings
from django.test import TestCase


class TestRecordViewExceptions(TestCase):

    @prevent_request_warnings  # suppress test output: Not Found: /catalogue/id/Z123456/
    def test_no_matches_respond_with_404(self):

        response = self.client.get("/catalogue/id/Z123456/")

        self.assertEqual(response.status_code, 404)

    @prevent_request_warnings  # suppress test output: Not Found: /catalogue/id/C123456/
    @responses.activate
    def test_empty_data_results_responds_with_resource_not_found_404(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/get?id=C123456",
            json={"data": []},
            status=200,
        )

        response = self.client.get("/catalogue/id/C123456/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.resolver_match.view_name, "details-page-machine-readable"
        )

    @prevent_request_warnings
    @responses.activate
    def test_unexpected_exception_responds_with_502(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/get?id=C123456",
            body=Exception("THIS IS AN UNKNOWN API EXCEPTION"),
        )

        with self.assertLogs(
            "app.lib.api", level="ERROR"
        ):  # assertLogs to suppress test console logging
            response = self.client.get("/catalogue/id/C123456/")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.context_data.get("exception_message"),
            "THIS IS AN UNKNOWN API EXCEPTION",
        )
