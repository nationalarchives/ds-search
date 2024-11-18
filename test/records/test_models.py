import json
from copy import deepcopy

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

    def test_iaid(self):

        self.record = Record(self.source)

        # patch raw data
        self.record._raw["@template"]["details"]["iaid"] = "C123456"

        self.assertEqual(self.record.iaid, "C123456")
