from app.records.models import Record
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

    def test_iaid(self):

        self.record = Record(self.source)

        # patch raw data
        self.record._raw["@template"]["details"]["iaid"] = "C123456"

        self.assertEqual(self.record.iaid, "C123456")

    def test_iaid_other_places(self):
        self.record = Record(self.source)
        # patch raw
        self.record._raw["@template"]["details"]["@previous"] = {
            "identifier": [
                {
                    "iaid": "C10298",
                },
            ],
        }
        self.record._raw["@template"]["details"]["@next"] = {
            "identifier": [
                {
                    "iaid": "C10296",
                },
            ],
        }
        self.record._raw["@template"]["details"]["parent"] = {
            "identifier": [
                {
                    "iaid": "C199",
                },
            ],
        }

        self.assertEqual(self.record.previous.iaid, "C10298")
        self.assertEqual(self.record.next.iaid, "C10296")
        self.assertEqual(self.record.parent.iaid, "C199")

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

    def test_reference_number(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["referenceNumber"] = "LO 2"
        self.assertEqual(self.record.reference_number, "LO 2")

    def test_reference_number_other_places(self):
        self.record = Record(self.source)
        # patch raw
        self.record._raw["@template"]["details"]["@previous"] = {
            "identifier": [
                {
                    "reference_number": "LO 3",
                },
            ],
        }
        self.record._raw["@template"]["details"]["@next"] = {
            "identifier": [
                {
                    "reference_number": "LO 1",
                },
            ],
        }
        self.record._raw["@template"]["details"]["parent"] = {
            "identifier": [
                {
                    "reference_number": "LO",
                },
            ],
        }

        self.assertEqual(self.record.previous.reference_number, "LO 3")
        self.assertEqual(self.record.next.reference_number, "LO 1")
        self.assertEqual(self.record.parent.reference_number, "LO")

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

    def test_summary_title(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "summaryTitle"
        ] = "This record has no title"
        self.assertEqual(self.record.summary_title, "This record has no title")

    def test_summary_title_other_places(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["@previous"] = {
            "summary": {
                "title": "Law Officers' Department: Patents for Inventions"
            },
        }
        self.record._raw["@template"]["details"]["@next"] = {
            "summary": {
                "title": "Law Officers' Department: Law Officers' Opinions"
            },
        }
        self.record._raw["@template"]["details"]["parent"] = {
            "summary": {
                "title": "Records created or inherited by the Law Officers' Department"
            },
        }
        self.record._raw["@template"]["details"]["@hierarchy"] = [
            {
                "identifier": [
                    {
                        "reference_number": "AIR",
                    }
                ],
                "summary": {
                    "title": "Records created or inherited by the Air Ministry, the Royal Air Force, and related..."
                },
            },
        ]
        self.assertEqual(
            self.record.hierarchy[0].summary_title,
            "Records created or inherited by the Air Ministry, the Royal Air Force, and related...",
        )

        self.assertEqual(
            self.record.previous.summary_title,
            "Law Officers' Department: Patents for Inventions",
        )
        self.assertEqual(
            self.record.next.summary_title,
            "Law Officers' Department: Law Officers' Opinions",
        )
        self.assertEqual(
            self.record.parent.summary_title,
            "Records created or inherited by the Law Officers' Department",
        )

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

    def test_level_code_other_places(self):
        self.record = Record(self.source)
        # patch raw
        self.record._raw["@template"]["details"]["@hierarchy"] = [
            {
                "identifier": [
                    {
                        "reference_number": "AIR",
                    }
                ],
                "level": {"code": 1},
            },
        ]
        self.assertEqual(self.record.hierarchy[0].level_code, 1)

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

    def test_closure_status(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "closureStatus"
        ] = "Open Document, Open Description"
        self.assertEqual(
            self.record.closure_status, "Open Document, Open Description"
        )

    def test_record_opening(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "recordOpening"
        ] = "01 September 2007"
        self.assertEqual(self.record.record_opening, "01 September 2007")

    def test_accruals(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "accruals"
        ] = "Series is accruing"
        self.assertEqual(self.record.accruals, "Series is accruing")

    def test_accumulation_dates(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "accumulationDates"
        ] = "File series began in 1971"
        self.assertEqual(
            self.record.accumulation_dates, "File series began in 1971"
        )

    def test_appraisal_information(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "appraisalInformation"
        ] = "Policy and contractual records have been preserved."
        self.assertEqual(
            self.record.appraisal_information,
            "Policy and contractual records have been preserved.",
        )

    def test_copies_information(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "copiesInformation"
        ] = "Microform copies are available on open access in Microfilm Reading Room (MRR) as FO 605. They must be ordered by this reference"
        self.assertEqual(
            self.record.copies_information,
            "Microform copies are available on open access in Microfilm Reading Room (MRR) as FO 605. They must be ordered by this reference",
        )

    def test_custodial_history(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "custodialHistory"
        ] = "Transferred to the Employment Department in 1988 and the Department for Education and Employment in 1995."
        self.assertEqual(
            self.record.custodial_history,
            "Transferred to the Employment Department in 1988 and the Department for Education and Employment in 1995.",
        )

    def test_immediate_source_of_acquisition(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "immediateSourceOfAcquisition"
        ] = [
            "since 1947 Essex Record Office",
            "Charles Cornwallis, 5th Baron Braybrooke, 1823-1902",
            "Henry Seymour Neville, 9th Baron Braybrooke, 1897-1990",
        ]
        self.assertEqual(
            self.record.immediate_source_of_acquisition,
            [
                "since 1947 Essex Record Office",
                "Charles Cornwallis, 5th Baron Braybrooke, 1823-1902",
                "Henry Seymour Neville, 9th Baron Braybrooke, 1897-1990",
            ],
        )

    def test_location_of_originals(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["locationOfOriginals"] = [
            "Museum of London Library",
            "Victoria & Albert Museum, Archive of Art and Design",
        ]
        self.assertEqual(
            self.record.location_of_originals,
            [
                "Museum of London Library",
                "Victoria & Albert Museum, Archive of Art and Design",
            ],
        )

    def test_restrictions_on_use(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "restrictionsOnUse"
        ] = "3 working days notice to produce"
        self.assertEqual(
            self.record.restrictions_on_use, "3 working days notice to produce"
        )

    def test_administrative_background(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "administrativeBackground"
        ] = "The Industrial Relations Department was set up as soon as the British Transport Commission began functioning and continued in existence until the end of the British Railway Board. In 1983 it was renamed Employee Relations Department."
        self.assertEqual(
            self.record.administrative_background,
            "The Industrial Relations Department was set up as soon as the British Transport Commission began functioning and continued in existence until the end of the British Railway Board. In 1983 it was renamed Employee Relations Department.",
        )

    def test_arrangement(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"][
            "arrangement"
        ] = "Former reference order within two accessions (AN 171/1-648 and AN 171/649-970)."
        self.assertEqual(
            self.record.arrangement,
            "Former reference order within two accessions (AN 171/1-648 and AN 171/649-970).",
        )

    def test_publication_note(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["publicationNote"] = [
            "Printed in Rymer's Foedera (1709 edition), viii 90-91.",
        ]
        self.assertEqual(
            self.record.publication_note,
            [
                "Printed in Rymer's Foedera (1709 edition), viii 90-91.",
            ],
        )

    def test_related_materials(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["relatedMaterials"] = [
            {
                "description": "Post December 1946 minutes in",
                "links": ['<a href="C5762">DEFE 4</a>'],
            }
        ]

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

    def test_description(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["description"] = (
            """C16248: Online descriptions of individual records can be viewed on Discovery, see <a class=\"extref\" href=\"f41eb-1496-446c-8bf8-21dc681223da\">RM 2</a>."""
            """"C16248: Also see the Royal Botanic Gardens, Kew <a class=\"extref\" href=\"https://www2.calmview.co.uk/kew/calmview/Record.aspx?src=CalmView.Catalog&amp;id=MN&amp;pos=1\">online catalogue</a>"""
            """C244: <span class=\"emph-italic\">Censuses of Population</span>"""
            """C244: <span class=\"list\"><span class=\"item\">Correspondence and papers</span></span>"""
        )
        self.assertEqual(
            self.record.description,
            (
                """C16248: Online descriptions of individual records can be viewed on Discovery, see <a class=\"extref\" href=\"f41eb-1496-446c-8bf8-21dc681223da\">RM 2</a>."""
                """"C16248: Also see the Royal Botanic Gardens, Kew <a class=\"extref\" href=\"https://www2.calmview.co.uk/kew/calmview/Record.aspx?src=CalmView.Catalog&amp;id=MN&amp;pos=1\">online catalogue</a>"""
                """C244: <span class=\"emph-italic\">Censuses of Population</span>"""
                """C244: <span class=\"list\"><span class=\"item\">Correspondence and papers</span></span>"""
            ),
        )

    def test_separated_materials(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["separatedMaterials"] = [
            {
                "description": "for 4 maps extracted from this item see",
                "links": [
                    '<a href="C8956177">MFQ 1/761/7</a>',
                    '<a href="C8956176">MFQ 1/761/6</a>',
                    '<a href="C8956175">MFQ 1/761/5</a>',
                    '<a href="C8956174">MFQ 1/761/4</a>',
                ],
            }
        ]

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

    def test_unpublished_finding_aids(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["unpublishedFindingAids"] = [
            "There is a general index in BT 4 . There is a subject index in BT 19.",
        ]
        self.assertEqual(
            self.record.unpublished_finding_aids,
            [
                "There is a general index in BT 4 . There is a subject index in BT 19.",
            ],
        )

    def test_hierarchy(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["@hierarchy"] = [
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
                "level": {"code": 2},
                "summary": {
                    "title": "Records of the Department of the Master General of Personnel and the Air Member for..."
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
                "summary": {"title": "Name: Percy Augustus Cecil Gadd."},
            },
        ]

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

    def test_next(self):
        self.record = Record(self.source)
        # patch raw data - C10297, LO 2
        self.record._raw["@template"]["details"]["@next"] = {
            "identifier": [
                {
                    "reference_number": "LO 1",
                },
                {
                    "iaid": "C10296",
                },
            ],
            "summary": {
                "title": "Law Officers' Department: Law Officers' Opinions"
            },
        }

        self.assertIsInstance(self.record.next, Record)
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

    def test_previous(self):
        self.record = Record(self.source)
        # patch raw data - C10297, LO 2
        self.record._raw["@template"]["details"]["@previous"] = {
            "identifier": [
                {
                    "reference_number": "LO 3",
                },
                {
                    "iaid": "C10298",
                },
            ],
            "summary": {
                "title": "Law Officers' Department: Patents for Inventions"
            },
        }

        self.assertIsInstance(self.record.previous, Record)
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

    def test_parent(self):
        self.record = Record(self.source)
        # patch raw data - C10297, LO 2
        self.record._raw["@template"]["details"]["parent"] = {
            "identifier": [
                {
                    "reference_number": "LO",
                },
                {
                    "iaid": "C199",
                },
            ],
            "summary": {
                "title": "Records created or inherited by the Law Officers' Department"
            },
        }

        self.assertIsInstance(self.record.parent, Record)
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

    def test_is_tna_true(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["groupArray"] = [
            {"value": "record"},
            {"value": "tna"},
        ]
        self.assertEqual(self.record.is_tna, True)

    def test_is_tna_false(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["groupArray"] = [
            {"value": "record"},
            {"value": "nonTna"},
        ]
        self.assertEqual(self.record.is_tna, False)

    def test_is_digitised_true(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["digitised"] = True
        self.assertEqual(self.record.is_digitised, True)

    def test_is_digitised_false(self):
        self.record = Record(self.source)
        # patch raw data
        self.record._raw["@template"]["details"]["digitised"] = False
        self.assertEqual(self.record.is_digitised, False)
