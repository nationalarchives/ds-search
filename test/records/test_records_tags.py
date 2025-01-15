from app.records.template_tags.records_tags import as_label
from django.test import SimpleTestCase
from jinja2 import Environment


class TestRecordsTags(SimpleTestCase):

    def test_configured_as_label(self):
        self.env = Environment()
        self.env.filters.update({"as_label": as_label})

        # a configured field label
        template = self.env.from_string("{{ 'reference_number' | as_label }}")
        self.assertEqual(template.render({}), "Reference")


    def test_unconfigured_as_label(self):
        self.env = Environment()
        self.env.filters.update({"as_label": as_label})

        # unconfigured field label
        template = self.env.from_string("{{ 'INVALID FIELD NAME' | as_label }}")
        self.assertEqual(template.render({}), "UNRECOGNISED FIELD NAME")
