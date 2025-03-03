import unittest

from config.jinja2 import qs_is_value_active, qs_toggle_value


class ContentParserTestCase(unittest.TestCase):
    def test_qs_is_value_active(self):
        TEST_QS = {"a": "1", "b": "2"}
        self.assertTrue(qs_is_value_active(TEST_QS, "a", "1"))
        self.assertTrue(qs_is_value_active(TEST_QS, "b", "2"))
        self.assertFalse(qs_is_value_active(TEST_QS, "a", "2"))
        self.assertFalse(qs_is_value_active(TEST_QS, "b", "1"))
        self.assertFalse(qs_is_value_active(TEST_QS, "c", "3"))
        # Handles empty query strings
        self.assertFalse(qs_is_value_active({}, "a", "1"))
        self.assertFalse(qs_is_value_active({}, "", ""))
        self.assertFalse(qs_is_value_active({"a": "1"}, "", ""))

    def test_qs_toggle_value(self):
        TEST_QS = {"a": "1", "b": "2"}
        # Adds a new qs
        self.assertEqual(
            "a=1&b=2&c=3", qs_toggle_value(TEST_QS.copy(), "c", "3")
        )
        # Changes an existing qs
        self.assertEqual("a=1&b=1", qs_toggle_value(TEST_QS.copy(), "b", "1"))
        # Removes a qs of the same value.
        self.assertEqual("b=2", qs_toggle_value(TEST_QS.copy(), "a", "1"))
        # Handle empty existing qs
        self.assertEqual("a=1", qs_toggle_value({}, "a", "1"))
