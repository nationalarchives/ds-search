from test.ciim.factories import create_record, create_response

import responses
from app.ciim.exceptions import (
    ClientAPIBadRequestError,
    ClientAPICommunicationError,
    ClientAPIInternalServerError,
    ClientAPIServiceUnavailableError,
    DoesNotExist,
    MultipleObjectsReturned,
)
from app.records.api import get_records_client
from app.records.models import Record
from django.conf import settings
from django.test import SimpleTestCase


class ClientGetTest(SimpleTestCase):
    def setUp(self):
        self.records_client = get_records_client()

    @responses.activate
    def test_raises_client_api_error_with_message(self):

        for label, value, expected in (
            (
                # label
                "Error Status 400",
                # value - API response
                {
                    "timestamp": "some value",
                    "status": "Bad Request",
                    "status_code": 400,
                    "message": "Identifier must be specified using 'id' query parameter",
                    "path": "/rosetta/data/get",
                },
                # expected - Client Exception, API message
                (
                    ClientAPIBadRequestError,
                    "Identifier must be specified using 'id' query parameter",
                ),
            ),
            (
                "Error Status 500",
                {
                    "timestamp": "some value",
                    "status": "Bad Request",
                    "status_code": 500,
                    "message": "Internal Server Error",
                    "path": "/rosetta/data/get",
                },
                (ClientAPIInternalServerError, "Internal Server Error"),
            ),
            (
                "Error Status 503",
                {
                    "timestamp": "some value",
                    "status": "Bad Request",
                    "status_code": 503,
                    "message": "failure to get a peer from the ring-balancer",
                    "path": "/rosetta/data/get",
                },
                (
                    ClientAPIServiceUnavailableError,
                    "failure to get a peer from the ring-balancer",
                ),
            ),
        ):
            with self.subTest(label):
                responses.add(
                    responses.GET,
                    f"{settings.CLIENT_BASE_URL}/get",
                    status=value.get("status_code"),
                    json=value,
                )

                with self.assertRaisesMessage(expected[0], expected[1]):
                    self.records_client.get()

    @responses.activate
    def test_default_exception(self):

        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            status=418,
            json={
                "message": "I'm a teapot",
            },
        )

        with self.assertRaisesMessage(
            ClientAPICommunicationError, "I'm a teapot"
        ):
            self.records_client.get()

    @responses.activate
    def test_raises_doesnotexist_when_empty_results_received(self):
        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            json=create_response(records=[]),
        )
        with self.assertRaisesMessage(
            DoesNotExist, "Id C123456 does not exist"
        ):
            self.records_client.get(id="C123456")

    @responses.activate
    def test_raises_multipleobjectsreturned_when_multiple_results_received(
        self,
    ):
        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            json=create_response(records=[create_record(), create_record()]),
        )
        with self.assertRaisesMessage(
            MultipleObjectsReturned, "Multiple records returned for Id C123456"
        ):
            self.records_client.get(id="C123456")

    @responses.activate
    def test_with_id_param(self):
        record_data = create_record(iaid="C198022")
        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            json=create_response(
                records=[
                    record_data,
                ]
            ),
        )
        result = self.records_client.get(id="C198022")

        self.assertIsInstance(result, Record)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.url,
            f"{settings.CLIENT_BASE_URL}/get?id=C198022",
        )
        self.assertEqual(
            result.iaid,
            record_data["@template"]["details"]["iaid"],
        )

    @responses.activate
    def test_decode_json_response(self):

        responses.add(
            responses.GET,
            f"{settings.CLIENT_BASE_URL}/get",
            status=204,  # no content
            body="",
            content_type="application/json",
        )

        with self.assertLogs("app.ciim.client", level="ERROR") as lc:
            with self.assertRaisesMessage(
                Exception, "Expecting value: line 1 column 1 (char 0)"
            ):
                self.records_client.get()
        self.assertIn(
            "ERROR:app.ciim.client:"
            "Expecting value: line 1 column 1 (char 0):"
            "Response body:",
            lc.output,
        )
