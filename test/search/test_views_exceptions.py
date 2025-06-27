from django.conf import settings
from django.test import TestCase, override_settings


class TestCatalogueSearchViewExceptions(TestCase):

    def setUp(self):
        # disable exception raised by client
        self.client.raise_request_exception = False

    @override_settings(
        ROSETTA_API_URL="",
    )
    def test_missing_config_with_server_error(self):

        with self.assertLogs("django.request", level="ERROR") as log:
            response = self.client.get("/catalogue/search/")

        self.assertIn("ROSETTA_API_URL not set", "".join(log.output))
        self.assertEqual(response.status_code, 500)

        # check content as it does not allow to test template SERVER_ERROR_TEMPLATE
        self.assertIn(
            "There is a problem with the service",
            response.content.decode("utf-8"),
        )
