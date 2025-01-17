from app.records.template_tags.records_tags import record_field_label
from django.test import SimpleTestCase
from jinja2 import Environment


class TestRecordsTags(SimpleTestCase):

    def test_configured_record_field_label(self):
        self.env = Environment()
        self.env.filters.update({"record_field_label": record_field_label})

        # a configured field label
        template = self.env.from_string(
            "{{ 'reference_number' | record_field_label }}"
        )
        self.assertEqual(template.render({}), "Reference")

    def test_unconfigured_record_field_label(self):
        self.env = Environment()
        self.env.filters.update({"record_field_label": record_field_label})

        # unconfigured field label
        template = self.env.from_string(
            "{{ 'INVALID FIELD NAME' | record_field_label }}"
        )
        self.assertEqual(template.render({}), "UNRECOGNISED FIELD NAME")
