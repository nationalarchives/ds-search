import json
from copy import deepcopy

from app.records.api import get_records_client
from app.records.models import Record
from django.conf import settings
from django.test import SimpleTestCase


class RecordModelTests(SimpleTestCase):
    maxDiff = None

    def setUp(self):

        # record structure
        self.source = {
            "@template": {"details": {}},
        }

    def test_empty_for_optional_attributes(self):
        self.record = Record(self.source)

        self.assertEqual(self.record.iaid, "")
        self.assertEqual(self.record.reference_number, "")
        self.assertEqual(self.record.summary_title, "")
        self.assertEqual(self.record.title, "")
        self.assertEqual(self.record.source, "")
        self.assertEqual(self.record.date_covering, "")
        self.assertEqual(self.record.creator, [])
        self.assertEqual(self.record.dimensions, "")
        self.assertEqual(self.record.former_department_reference, "")
        self.assertEqual(self.record.former_pro_reference, "")
        self.assertEqual(self.record.language, "")
        self.assertEqual(self.record.legal_status, "")
        self.assertEqual(self.record.level, "")
        self.assertEqual(self.record.level_code, None)
        self.assertEqual(self.record.map_designation, "")
        self.assertEqual(self.record.map_scale, "")
        self.assertEqual(self.record.note, "")
        self.assertEqual(self.record.physical_condition, "")
        self.assertEqual(self.record.physical_description, "")
        self.assertEqual(self.record.held_by, "")
        self.assertEqual(self.record.held_by_id, "")
        self.assertEqual(self.record.held_by_url, "")
        self.assertEqual(self.record.access_condition, "")

    def test_iaid(self):

        self.record = Record(self.source)

        # patch raw data
        self.record._raw["@template"]["details"]["iaid"] = "C123456"

        self.assertEqual(self.record.iaid, "C123456")

    def test_reference_number(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["referenceNumber"] = "LO 2"
        self.assertEqual(self.record.reference_number, "LO 2")

    def test_summary_title(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "summaryTitle"
        ] = "This record has no title"
        self.assertEqual(self.record.summary_title, "This record has no title")

    def test_title(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["title"] = (
            "Ministry of Defence: Joint Intelligence Bureau and Defence Intelligence Staff: "
            "Intelligence Conferences, Committees and Working Parties: Reports and Papers."
        )
        self.assertEqual(
            self.record.title,
            (
                "Ministry of Defence: Joint Intelligence Bureau and Defence Intelligence Staff: "
                "Intelligence Conferences, Committees and Working Parties: Reports and Papers."
            ),
        )

    def test_source(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["source"] = "CAT"
        self.assertEqual(self.record.source, "CAT")

    def test_custom_record_type(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["source"] = "CAT"
        self.assertEqual(self.record.custom_record_type, "CAT")

    def test_date_covering(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["dateCovering"] = "2015-07-31"
        self.assertEqual(self.record.date_covering, "2015-07-31")

    def test_creator(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["creator"] = [
            "Donop, Stanley Brenton, 1860-1941",
            "Lambart, Frederick Rudolph, 1865-1946",
            "Thomson, William Montgomerie, 1877-1963",
        ]
        self.assertEqual(
            self.record.creator,
            [
                "Donop, Stanley Brenton, 1860-1941",
                "Lambart, Frederick Rudolph, 1865-1946",
                "Thomson, William Montgomerie, 1877-1963",
            ],
        )

    def test_dimensions(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "dimensions"
        ] = "63.5 cm x 68.5 cm"
        self.assertEqual(self.record.dimensions, "63.5 cm x 68.5 cm")

    def test_former_department_reference(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "formerDepartmentReference"
        ] = "African No. 355"
        self.assertEqual(
            self.record.former_department_reference, "African No. 355"
        )

    def test_former_pro_reference(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "formerProReference"
        ] = "ASSI 35"
        self.assertEqual(self.record.former_pro_reference, "ASSI 35")

    def test_language(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "language"
        ] = "Chinese, English, Malay and Tamil"
        self.assertEqual(
            self.record.language, "Chinese, English, Malay and Tamil"
        )

    def test_legal_status(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "legalStatus"
        ] = "Public Record(s)"
        self.assertEqual(self.record.legal_status, "Public Record(s)")

    def test_level(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["level"] = {
            "code": 7,
            "value": "Item",
        }
        self.assertEqual(self.record.level, "Item")

    def test_level_code(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["level"] = {
            "code": 7,
            "value": "Item",
        }
        self.assertEqual(self.record.level_code, 7)

    def test_map_designation(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "mapDesignation"
        ] = "OS 1:2500 County Series"
        self.assertEqual(self.record.map_designation, "OS 1:2500 County Series")

    def test_map_scale(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["mapScale"] = "1:2500"
        self.assertEqual(self.record.map_scale, "1:2500")

    def test_note(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["note"] = (
            "Details have been added from C 32/18, which also gives "
            "information about further process."
        )
        self.assertEqual(
            self.record.note,
            "Details have been added from C 32/18,"
            " which also gives information about further process.",
        )

    def test_physical_condition(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "physicalCondition"
        ] = "In ink, on tracing linen"
        self.assertEqual(
            self.record.physical_condition, "In ink, on tracing linen"
        )

    def test_physical_description(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "physicalDescription"
        ] = "file(s)"
        self.assertEqual(self.record.physical_description, "file(s)")

    def test_held_by(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "heldBy"
        ] = "National Maritime Museum"
        self.assertEqual(self.record.held_by, "National Maritime Museum")

    def test_held_by_id(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["heldById"] = "A13530841"
        self.assertEqual(self.record.held_by_id, "A13530841")

    def test_held_by_url(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["heldById"] = "A13530841"
        self.assertEqual(self.record.held_by_url, "/catalogue/id/A13530841/")

    def test_access_condition(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "accessCondition"
        ] = "Subject to 30 year closure"
        self.assertEqual(
            self.record.access_condition, "Subject to 30 year closure"
        )


class CatalogueRecordResponseTests(SimpleTestCase):
    """
    Tests for typical responses for differrent id formats
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.records_client = get_records_client()

    def test_response_C15836(self):
        fixture_path = (
            f"{settings.BASE_DIR}/test/records/fixtures/response_C15836.json"
        )
        with open(fixture_path, "r") as f:
            fixture_contents = json.loads(f.read())

        self.record = Record(deepcopy(fixture_contents["data"][0]))

        self.assertEqual(self.record.iaid, "C15836")
        self.assertEqual(self.record.source, "CAT")
        self.assertEqual(self.record.custom_record_type, "CAT")
        self.assertEqual(self.record.date_covering, "1959 - 1975")
        self.assertEqual(self.record.creator, ["Ministry of Defence, 1947"])
        self.assertEqual(self.record.dimensions, "")
        self.assertEqual(self.record.former_department_reference, "EWP, DI")
        self.assertEqual(self.record.former_pro_reference, "")
        self.assertEqual(self.record.language, "English")
        self.assertEqual(self.record.legal_status, "Public Record(s)")
        self.assertEqual(self.record.level, "Series")
        self.assertEqual(self.record.level_code, 3)
        self.assertEqual(self.record.map_designation, "")
        self.assertEqual(self.record.map_scale, "")
        self.assertEqual(self.record.note, "")
        self.assertEqual(self.record.physical_condition, "")
        self.assertEqual(self.record.physical_description, "7 file(s)")
        self.assertEqual(self.record.held_by, "The National Archives, Kew")
        self.assertEqual(self.record.held_by_id, "A13530124")
        self.assertEqual(self.record.held_by_url, "/catalogue/id/A13530124/")
        self.assertEqual(
            self.record.access_condition, "Subject to 30 year closure"
        )

    def test_response_00149557ca64456a8a41e44f14621801_1(self):
        fixture_path = (
            f"{settings.BASE_DIR}"
            "/test/records/fixtures/response_00149557ca64456a8a41e44f14621801_1.json"
        )
        with open(fixture_path, "r") as f:
            fixture_contents = json.loads(f.read())
        self.record = Record(deepcopy(fixture_contents["data"][0]))
        self.assertEqual(self.record.iaid, "00149557ca64456a8a41e44f14621801_1")
        self.assertEqual(self.record.source, "CAT")
        self.assertEqual(self.record.custom_record_type, "CAT")
        self.assertEqual(self.record.date_covering, "2015-07-31")
        self.assertEqual(self.record.creator, [])
        self.assertEqual(self.record.dimensions, "")
        self.assertEqual(self.record.former_department_reference, "")
        self.assertEqual(self.record.former_pro_reference, "")
        self.assertEqual(self.record.language, "")
        self.assertEqual(self.record.legal_status, "Public Record")
        self.assertEqual(self.record.level, "Piece")
        self.assertEqual(self.record.level_code, 6)
        self.assertEqual(self.record.map_designation, "")
        self.assertEqual(self.record.map_scale, "")
        self.assertEqual(self.record.note, "")
        self.assertEqual(self.record.physical_condition, "")
        self.assertEqual(self.record.physical_description, "1 digital record")
        self.assertEqual(self.record.held_by, "The National Archives, Kew")
        self.assertEqual(self.record.held_by_id, "A13530124")
        self.assertEqual(self.record.held_by_url, "/catalogue/id/A13530124/")
        self.assertEqual(self.record.access_condition, "Open on Transfer")
