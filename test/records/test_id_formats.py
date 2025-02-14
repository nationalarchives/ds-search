import re

from app.records.converters import IDConverter
from django.test import SimpleTestCase


class TestIDFormats(SimpleTestCase):
    def test_valid_formats(self):
        id_regex = re.compile(IDConverter.regex)
        for label, value in (
            ("longformat", "3717ee38900740728076a61a398fcb84"),
            ("guid", "4d8dae2c-b417-4614-8ed8-924b9b4beeac"),
            ("guid-ish 1", "c5f5-0f02-4d03-9b5c-8ec7973794b7"),
            ("guid-ish 2", "d7b-e1c2-45b2-83dc-17df01b13e7e"),
            ("guid-ish 3", "f0-dab7f878b99b"),
            ("dri_guid_plus", "00149557ca64456a8a41e44f14621801_1"),
            ("iaid_A", "A13530124"),
            ("iaid_C", "C2341693"),
            ("iaid_D", "D431198"),
            ("iaid_F", "F257629"),
            ("iaid_N", "N14562581"),
        ):
            with self.subTest(label):
                self.assertTrue(id_regex.match(value))
