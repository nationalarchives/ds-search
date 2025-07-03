from http import HTTPStatus

from django.test import TestCase, override_settings


class TestCatalogueSearchViewExceptions(TestCase):

    @override_settings(
        ROSETTA_API_URL="",
    )
    def test_missing_config_with_server_error(self):

        with self.assertLogs("app.errors.middleware", level="ERROR") as log:
            response = self.client.get("/catalogue/search/")

        self.assertIn("ROSETTA_API_URL not set", "".join(log.output))
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

        # check content as raising exception does not allow to test template
        self.assertIn(
            "There is a problem with the service",
            response.content.decode("utf-8"),
        )
