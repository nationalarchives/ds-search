from test.ciim.factories import create_record, create_response

import responses
from app.records.api import get_records_client
from app.records.models import Record
from django.conf import settings
from django.test import SimpleTestCase


class APIModelTest(SimpleTestCase):
    def setUp(self):
        self.records_client = get_records_client()

    @responses.activate
    def test_record_instance(self):
        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            json=create_response(
                records=[
                    create_record(iaid="C198022"),
                ]
            ),
        )
        result = self.records_client.get(id="C198022")

        self.assertIsInstance(result, Record)
