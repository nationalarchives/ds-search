import logging

from app.records.models import Record
from django.test import SimpleTestCase


class RecordModelTests(SimpleTestCase):
    maxDiff = None

    def setUp(self):
        # record structure
        self.source = {
            "@template": {
                "details": {
                    "iaid": "C123456",
                    "title": "Ministry of Defence: Joint Intelligence Bureau and Defence Intelligence Staff: Intelligence Conferences, Committees and Working Parties: Reports and Papers.",
                    "summaryTitle": "This record has no title",
                    "dateCovering": "2015-07-31",
                    "source": "CAT",
                    "referenceNumber": "LO 2",
                    "creator": [
                        "Donop, Stanley Brenton, 1860-1941",
                        "Lambart, Frederick Rudolph, 1865-1946",
                        "Thomson, William Montgomerie, 1877-1963",
                    ],
                    "formerDepartmentReference": "African No. 355",
                    "dimensions": "63.5 cm x 68.5 cm",
                    "language": "Chinese, English, Malay and Tamil",
                    "formerProReference": "ASSI 35",
                    "legalStatus": "Public Record(s)",
                    "level": {"code": 7, "value": "Item"},
                    "mapDesignation": "OS 1:2500 County Series",
                    "mapScale": "1:2500",
                    "note": "Details have been added from C 32/18, which also gives information about further process.",
                    "physicalCondition": "In ink, on tracing linen",
                    "physicalDescription": "file(s)",
                    "heldBy": "National Maritime Museum",
                    "heldById": "A13530841",
                    "accessCondition": "Subject to 30 year closure",
                    "closureStatus": "Open Document, Open Description",
                    "recordOpening": "01 September 2007",
                    "accruals": "Series is accruing",
                    "accumulationDates": "File series began in 1971",
                    "appraisalInformation": "Policy and contractual records have been preserved.",
                    "copiesInformation": "Microform copies are available on open access in Microfilm Reading Room (MRR) as FO 605. They must be ordered by this reference",
                    "custodialHistory": "Transferred to the Employment Department in 1988 and the Department for Education and Employment in 1995.",
                    "immediateSourceOfAcquisition": [
                        "since 1947 Essex Record Office",
                        "Charles Cornwallis, 5th Baron Braybrooke, 1823-1902",
                        "Henry Seymour Neville, 9th Baron Braybrooke, 1897-1990",
                    ],
                    "locationOfOriginals": [
                        "Museum of London Library",
                        "Victoria & Albert Museum, Archive of Art and Design",
                    ],
                    "restrictionsOnUse": "3 working days notice to produce",
                    "administrativeBackground": "The Industrial Relations Department was set up as soon as the British Transport Commission began functioning and continued in existence until the end of the British Railway Board. In 1983 it was renamed Employee Relations Department.",
                    "arrangement": "Former reference order within two accessions (AN 171/1-648 and AN 171/649-970).",
                    "publicationNote": [
                        "Printed in Rymer's Foedera (1709 edition), viii 90-91.",
                    ],
                    "relatedMaterials": [
                        {
                            "description": "Post December 1946 minutes in",
                            "links": ['<a href="C5762">DEFE 4</a>'],
                        }
                    ],
                    "description": """C16248: Online descriptions of individual records can be viewed on Discovery, see <a class=\"extref\" href=\"f41eb-1496-446c-8bf8-21dc681223da\">RM 2</a>.""",
                    "separatedMaterials": [
                        {
                            "description": "for 4 maps extracted from this item see",
                            "links": [
                                '<a href="C8956177">MFQ 1/761/7</a>',
                                '<a href="C8956176">MFQ 1/761/6</a>',
                                '<a href="C8956175">MFQ 1/761/5</a>',
                                '<a href="C8956174">MFQ 1/761/4</a>',
                            ],
                        }
                    ],
                    "unpublishedFindingAids": [
                        "There is a general index in BT 4 . There is a subject index in BT 19.",
                    ],
                    "@previous": {
                        "identifier": [
                            {
                                "iaid": "C10298",
                                "reference_number": "LO 3",
                            },
                        ],
                        "summary": {
                            "title": "Law Officers' Department: Patents for Inventions"
                        },
                    },
                    "@next": {
                        "identifier": [
                            {
                                "iaid": "C10296",
                                "reference_number": "LO 1",
                            },
                        ],
                        "summary": {
                            "title": "Law Officers' Department: Law Officers' Opinions"
                        },
                    },
                    "parent": {
                        "identifier": [
                            {
                                "iaid": "C199",
                                "reference_number": "LO",
                            },
                        ],
                        "summary": {
                            "title": "Records created or inherited by the Law Officers' Department"
                        },
                    },
                    "@hierarchy": [
                        {
                            "identifier": [
                                {
                                    "reference_number": "AIR",
                                }
                            ],
                            "level": {"code": 1},
                            "summary": {
                                "title": "Records created or inherited by the Air Ministry, the Royal Air Force, and related..."
                            },
                        },
                        {
                            "identifier": [
                                {
                                    "reference_number": "AIR 79",
                                }
                            ],
                            "level": {"code": 3},
                            "summary": {
                                "title": "Air Ministry: Air Member for Personnel and predecessors: Airmen's Records"
                            },
                        },
                        {
                            "identifier": [
                                {
                                    "reference_number": "AIR 79/962",
                                }
                            ],
                            "level": {"code": 6},
                            "summary": {
                                "title": "107079 - 107200 (Described at item level)."
                            },
                        },
                        {
                            "identifier": [
                                {
                                    "reference_number": "AIR 79/962/107133",
                                }
                            ],
                            "level": {"code": 7},
                            "summary": {
                                "title": "Name: Percy Augustus Cecil Gadd."
                            },
                        },
                    ],
                    "groupArray": [
                        {"value": "record"},
                        {"value": "tna"},
                    ],
                    "digitised": True,
                }
            },
        }

    def test_empty_for_optional_attributes(self):
        self.record = Record(
            {
                "@template": {"details": {}},
            }
        )

        self.assertEqual(self.record.iaid, "")
        self.assertEqual(self.record.source, "")
        self.assertEqual(self.record.custom_record_type, "")
        self.assertEqual(self.record.reference_number, "")
        self.assertEqual(self.record.title, "")
        self.assertEqual(self.record.summary_title, "")
        self.assertEqual(self.record.date_covering, "")
        self.assertEqual(self.record.creator, [])
        self.assertEqual(self.record.dimensions, "")
        self.assertEqual(self.record.former_department_reference, "")
        self.assertEqual(self.record.former_pro_reference, "")
        self.assertEqual(self.record.language, "")
        self.assertEqual(self.record.legal_status, "")
        self.assertEqual(self.record.level, "")
        self.assertEqual(self.record.level_code, "")
        self.assertEqual(self.record.map_designation, "")
        self.assertEqual(self.record.map_scale, "")
        self.assertEqual(self.record.note, "")
        self.assertEqual(self.record.physical_condition, "")
        self.assertEqual(self.record.physical_description, "")
        self.assertEqual(self.record.held_by, "")
        self.assertEqual(self.record.held_by_id, "")
        self.assertEqual(self.record.held_by_url, "")
        self.assertEqual(self.record.access_condition, "")
        self.assertEqual(self.record.closure_status, "")
        self.assertEqual(self.record.record_opening, "")
        self.assertEqual(self.record.accruals, "")
        self.assertEqual(self.record.accumulation_dates, "")
        self.assertEqual(self.record.appraisal_information, "")
        self.assertEqual(self.record.copies_information, "")
        self.assertEqual(self.record.custodial_history, "")
        self.assertEqual(self.record.immediate_source_of_acquisition, [])
        self.assertEqual(self.record.location_of_originals, [])
        self.assertEqual(self.record.restrictions_on_use, "")
        self.assertEqual(self.record.administrative_background, "")
        self.assertEqual(self.record.arrangement, "")
        self.assertEqual(self.record.publication_note, [])
        self.assertEqual(self.record.related_materials, ())
        self.assertEqual(self.record.description, "")
        self.assertEqual(self.record.separated_materials, ())
        self.assertEqual(self.record.unpublished_finding_aids, [])
        self.assertEqual(self.record.hierarchy, ())
        self.assertEqual(self.record.next, None)
        self.assertEqual(self.record.previous, None)
        self.assertEqual(self.record.parent, None)
        self.assertEqual(self.record.is_tna, False)
        self.assertEqual(self.record.is_digitised, False)

    def test_properties(self):
        self.record = Record(self.source)
        self.assertEqual(self.record.iaid, "C123456")
        self.assertEqual(self.record.previous.iaid, "C10298")
        self.assertEqual(self.record.next.iaid, "C10296")
        self.assertEqual(self.record.parent.iaid, "C199")
        self.assertEqual(self.record.source, "CAT")
        self.assertEqual(self.record.custom_record_type, "CAT")
        self.assertEqual(self.record.reference_number, "LO 2")
        self.assertEqual(
            self.record.title,
            (
                "Ministry of Defence: Joint Intelligence Bureau and Defence Intelligence Staff: "
                "Intelligence Conferences, Committees and Working Parties: Reports and Papers."
            ),
        )
        self.assertEqual(self.record.summary_title, "This record has no title")
        self.assertEqual(self.record.date_covering, "2015-07-31")
        self.assertEqual(
            self.record.creator,
            [
                "Donop, Stanley Brenton, 1860-1941",
                "Lambart, Frederick Rudolph, 1865-1946",
                "Thomson, William Montgomerie, 1877-1963",
            ],
        )
        self.assertEqual(self.record.dimensions, "63.5 cm x 68.5 cm")
        self.assertEqual(
            self.record.former_department_reference, "African No. 355"
        )
        self.assertEqual(
            self.record.language, "Chinese, English, Malay and Tamil"
        )
        self.assertEqual(self.record.former_pro_reference, "ASSI 35")
        self.assertEqual(self.record.legal_status, "Public Record(s)")
        self.assertEqual(self.record.level, "Item")
        self.assertEqual(self.record.level_code, 7)
        self.assertEqual(self.record.map_designation, "OS 1:2500 County Series")
        self.assertEqual(self.record.map_scale, "1:2500")
        self.assertEqual(
            self.record.note,
            "Details have been added from C 32/18, which also gives information about further process.",
        )
        self.assertEqual(
            self.record.physical_condition, "In ink, on tracing linen"
        )
        self.assertEqual(self.record.physical_description, "file(s)")
        self.assertEqual(self.record.held_by, "National Maritime Museum")
        self.assertEqual(self.record.held_by_id, "A13530841")
        self.assertEqual(self.record.held_by_url, "/catalogue/id/A13530841/")
        self.assertEqual(
            self.record.access_condition, "Subject to 30 year closure"
        )
        self.assertEqual(
            self.record.closure_status, "Open Document, Open Description"
        )
        self.assertEqual(self.record.record_opening, "01 September 2007")
        self.assertEqual(self.record.accruals, "Series is accruing")
        self.assertEqual(
            self.record.accumulation_dates, "File series began in 1971"
        )
        self.assertEqual(
            self.record.appraisal_information,
            "Policy and contractual records have been preserved.",
        )
        self.assertEqual(
            self.record.copies_information,
            (
                "Microform copies are available on open access in Microfilm "
                "Reading Room (MRR) as FO 605. They must be ordered by this reference"
            ),
        )
        self.assertEqual(
            self.record.custodial_history,
            "Transferred to the Employment Department in 1988 and the Department for Education and Employment in 1995.",
        )
        self.assertEqual(
            self.record.immediate_source_of_acquisition,
            [
                "since 1947 Essex Record Office",
                "Charles Cornwallis, 5th Baron Braybrooke, 1823-1902",
                "Henry Seymour Neville, 9th Baron Braybrooke, 1897-1990",
            ],
        )
        self.assertEqual(
            self.record.location_of_originals,
            [
                "Museum of London Library",
                "Victoria & Albert Museum, Archive of Art and Design",
            ],
        )
        self.assertEqual(
            self.record.restrictions_on_use, "3 working days notice to produce"
        )
        self.assertEqual(
            self.record.administrative_background,
            (
                "The Industrial Relations Department was set up as soon as the "
                "British Transport Commission began functioning and continued in "
                "existence until the end of the British Railway Board. In 1983 it "
                "was renamed Employee Relations Department."
            ),
        )
        self.assertEqual(
            self.record.arrangement,
            "Former reference order within two accessions (AN 171/1-648 and AN 171/649-970).",
        )
        self.assertEqual(
            self.record.publication_note,
            [
                "Printed in Rymer's Foedera (1709 edition), viii 90-91.",
            ],
        )
        self.assertEqual(
            self.record.related_materials,
            (
                {
                    "description": "Post December 1946 minutes in",
                    "links": [
                        {
                            "id": "C5762",
                            "href": "/catalogue/id/C5762/",
                            "text": "DEFE 4",
                        }
                    ],
                },
            ),
        )
        self.assertEqual(
            self.record.description,
            """C16248: Online descriptions of individual records can be viewed on Discovery, see <a class=\"extref\" href=\"f41eb-1496-446c-8bf8-21dc681223da\">RM 2</a>.""",
        )
        self.assertEqual(
            self.record.separated_materials,
            (
                {
                    "description": "for 4 maps extracted from this item see",
                    "links": [
                        {
                            "id": "C8956177",
                            "href": "/catalogue/id/C8956177/",
                            "text": "MFQ 1/761/7",
                        },
                        {
                            "id": "C8956176",
                            "href": "/catalogue/id/C8956176/",
                            "text": "MFQ 1/761/6",
                        },
                        {
                            "id": "C8956175",
                            "href": "/catalogue/id/C8956175/",
                            "text": "MFQ 1/761/5",
                        },
                        {
                            "id": "C8956174",
                            "href": "/catalogue/id/C8956174/",
                            "text": "MFQ 1/761/4",
                        },
                    ],
                },
            ),
        )
        self.assertEqual(
            self.record.unpublished_finding_aids,
            [
                "There is a general index in BT 4 . There is a subject index in BT 19.",
            ],
        )
        self.assertEqual(len(self.record.hierarchy), 4)
        for r in self.record.hierarchy:
            self.assertIsInstance(r, Record)
            self.assertEqual(
                [
                    (r.level_code, r.reference_number, r.summary_title)
                    for r in self.record.hierarchy
                ],
                [
                    (
                        1,
                        "AIR",
                        "Records created or inherited by the Air Ministry, the Royal Air Force, and related...",
                    ),
                    (
                        3,
                        "AIR 79",
                        "Air Ministry: Air Member for Personnel and predecessors: Airmen's Records",
                    ),
                    (
                        6,
                        "AIR 79/962",
                        "107079 - 107200 (Described at item level).",
                    ),
                    (
                        7,
                        "AIR 79/962/107133",
                        "Name: Percy Augustus Cecil Gadd.",
                    ),
                ],
            )
        self.assertEqual(
            (
                self.record.next.iaid,
                self.record.next.reference_number,
                self.record.next.summary_title,
            ),
            (
                "C10296",
                "LO 1",
                "Law Officers' Department: Law Officers' Opinions",
            ),
        )
        self.assertEqual(
            (
                self.record.previous.iaid,
                self.record.previous.reference_number,
                self.record.previous.summary_title,
            ),
            (
                "C10298",
                "LO 3",
                "Law Officers' Department: Patents for Inventions",
            ),
        )
        self.assertEqual(
            (
                self.record.parent.iaid,
                self.record.parent.reference_number,
                self.record.parent.summary_title,
            ),
            (
                "C199",
                "LO",
                "Records created or inherited by the Law Officers' Department",
            ),
        )
        self.assertEqual(self.record.is_tna, True)
        self.assertEqual(self.record.is_digitised, True)

    def test_invalid_data_for_held_by_url(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["iaid"] = "C12345"
        self.record._raw["@template"]["details"]["heldById"] = "INVALID"

        with self.assertLogs("app.records.models", level="WARNING") as lc:
            result = self.record.held_by_url
        self.assertEqual(self.record.held_by_url, result)
        self.assertIn(
            "WARNING:app.records.models:held_by_url:Record(C12345):No reverse match for details-page-machine-readable with held_by_id=INVALID",
            lc.output,
        )
