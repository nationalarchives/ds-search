from http import HTTPStatus
from test.utils import prevent_request_warnings

import responses
from django.conf import settings
from django.test import TestCase, override_settings


class TestRecordViewExceptions(TestCase):

    def setUp(self):
        # disable exception raised by client
        self.client.raise_request_exception = False

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

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.resolver_match.view_name, "records:details")

    @prevent_request_warnings
    @responses.activate
    def test_unexpected_exception_responds_with_server_error_500(self):

        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/get?id=C123456",
            body=Exception("THIS IS AN UNKNOWN API EXCEPTION"),
        )

        with self.assertLogs("django.request", level="ERROR") as log:
            response = self.client.get("/catalogue/id/C123456/")

        self.assertIn("THIS IS AN UNKNOWN API EXCEPTION", "".join(log.output))
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

        # check content as raising exception does not allow to test template
        self.assertIn(
            "There is a problem with the service",
            response.content.decode("utf-8"),
        )

    @override_settings(
        ROSETTA_API_URL="",
    )
    def test_missing_config_responds_with_server_error_500(self):

        with self.assertLogs("django.request", level="ERROR") as log:
            response = self.client.get("/catalogue/id/C123456/")

        self.assertIn("ROSETTA_API_URL not set", "".join(log.output))
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

        # check content as raising exception does not allow to test template
        self.assertIn(
            "There is a problem with the service",
            response.content.decode("utf-8"),
        )
