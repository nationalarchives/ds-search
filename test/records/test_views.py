from test.ciim.factories import create_record, create_response

import responses
from django.conf import settings
from django.test import TestCase


class TestRecordView(TestCase):

    def test_no_matches_respond_with_404(self):

        response = self.client.get("/catalogue/id/Z123456/")

        self.assertEqual(response.status_code, 404)

    @responses.activate
    def test_empty_results_responds_with_404(self):
        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            json=create_response(records=[]),
        )

        response = self.client.get("/catalogue/id/C123456/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.resolver_match.view_name, "details-page-machine-readable"
        )

    @responses.activate
    def test_record_rendered_for_single_result(self):

        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            json=create_response(
                records=[
                    create_record(iaid="C123456"),
                ]
            ),
        )

        response = self.client.get("/catalogue/id/C123456/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.view_name, "details-page-machine-readable"
        )
        self.assertTemplateUsed("records/record_detail.html")

        # context attributes
        self.assertEqual(
            response.context_data.get("page_type"), "Record details page"
        )
        self.assertEqual(
            response.context_data.get("page_title"), "Catalogue ID: C123456"
        )
