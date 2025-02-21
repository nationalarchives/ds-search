import responses
from app.lib.api import JSONAPIClient, ResourceNotFound
from app.records.api import record_details_by_id
from app.records.models import Record
from django.conf import settings
from django.test import SimpleTestCase


class TestRecordDetailsById(SimpleTestCase):
    def setUp(self):
        self.records_client = JSONAPIClient

    @responses.activate
    def test_record_details_by_id_returns_record(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/get?id=C198022",
            json={"data": [{"@template": {"details": {"iaid": "C198022"}}}]},
            status=200,
        )
        result = record_details_by_id(id="C198022")

        self.assertIsInstance(result, Record)

    @responses.activate
    def test_no_data_returned_for_id(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/get?id=C198022",
            json={},
            status=200,
        )

        with self.assertRaisesMessage(
            Exception, "No data returned for id C198022"
        ):
            _ = record_details_by_id(id="C198022")

    @responses.activate
    def test_resource_not_found_id_does_not_exist(self):
        responses.add(
            responses.GET,
            f"{settings.ROSETTA_API_URL}/get?id=C198022",
            json={"data": []},
            status=200,
        )

        with self.assertRaisesMessage(
            ResourceNotFound, "id C198022 does not exist"
        ):
            _ = record_details_by_id(id="C198022")
