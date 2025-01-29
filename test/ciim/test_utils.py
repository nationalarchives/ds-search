from datetime import date

from app.ciim.utils import ValueExtractionError, extract, format_link
from django.test import SimpleTestCase

TODAY = date.today()


class TestExtract(SimpleTestCase):
    test_data = {
        "item": {
            "id": 2,
            "name": "foo",
            "date_created": TODAY,
            "parent": {
                "id": 1,
                "name": "parent",
                "date_created": TODAY,
            },
            "children": [
                {"id": 3, "name": "bar", "date_created": TODAY},
                {"id": 4, "name": "baz", "date_created": TODAY},
            ],
        }
    }

    def test_successes(self):
        """
        Show that we can extract values via:
        - dict keys
        - sequence indexes
        - object attribute names
        """
        for key, expected_value in (
            ("item", self.test_data["item"]),
            ("item.id", 2),
            ("item.date_created", TODAY),
            ("item.date_created.day", TODAY.day),
            ("item.parent.id", 1),
            ("item.parent.date_created.year", TODAY.year),
            ("item.children.0.id", 3),
            ("item.children.0.date_created.month", TODAY.month),
            ("item.children.1.id", 4),
            ("item.children.1.date_created.month", TODAY.month),
        ):
            with self.subTest(key):
                self.assertEqual(
                    extract(self.test_data, key),
                    expected_value,
                )

    def test_without_defaults(self):
        """
        Shows that wherever in the process the failure happens, it is
        reported as a ValueExtractionError with a useful description.
        """
        for key, problematic_bit, error_class in (
            ("item_2", "item_2", KeyError),
            ("item.invalid_key", "invalid_key", KeyError),
            ("item.date_created.invalid_attr", "invalid_attr", AttributeError),
            ("item.children.invalid_index", "invalid_index", AttributeError),
            ("item.children.999", "999", IndexError),
            ("item.children.1.invalid_key", "invalid_key", KeyError),
            (
                "item.children.1.date_created.invalid_attr",
                "invalid_attr",
                AttributeError,
            ),
        ):
            with self.subTest(key):
                msg_part = (
                    f"{error_class} raised when extracting '{problematic_bit}'"
                )
                with self.assertRaisesRegex(ValueExtractionError, msg_part):
                    extract(self.test_data, key)

    def test_with_defaults(self):
        """
        Shows that wherever in the process the failure happens, no exception
        is raised, and the default value is returned.
        """
        for key, default_value in (
            ("item_2", "somestring"),
            ("item.invalid_key", 1),
            ("item.date_created.invalid_attr", None),
            ("item.children.invalid_index", TODAY),
            ("item.children.999", None),
            ("item.children.1.invalid_key", False),
            ("item.children.1.date_created.invalid_attr", True),
        ):
            with self.subTest(key):
                self.assertIs(
                    extract(self.test_data, key, default=default_value),
                    default_value,
                )


class TestFormatLink(SimpleTestCase):

    def test_format_link(self):

        test_data = (
            (
                "valid link",
                '<a href="C5789">DEFE 31</a>',
                {
                    "id": "C5789",
                    "href": "/catalogue/id/C5789/",
                    "text": "DEFE 31",
                },
            ),
        )

        for label, value, expected in test_data:
            with self.subTest(label):
                result = format_link(value)
                self.assertEqual(result, expected)

    def test_format_link_with_invalid_data(self):

        test_data = (
            (
                "invalid id",
                '<a href="INVALID">some value</a>',
                (
                    {"id": "INVALID", "href": "", "text": "some value"},
                    "WARNING:app.ciim.utils:format_link:No reverse match for details-page-machine-readable with id=INVALID",
                ),
            ),
            (
                "missing id",
                "some value",
                (
                    {"id": "", "href": "", "text": "some value"},
                    "WARNING:app.ciim.utils:format_link:No reverse match for details-page-machine-readable with id=None",
                ),
            ),
        )

        for label, value, expected in test_data:
            with self.subTest(label):
                with self.assertLogs("app.ciim.utils", level="WARNING") as lc:
                    result = format_link(value)
                self.assertIn(expected[1], lc.output)
                self.assertEqual(result, expected[0])
