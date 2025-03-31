import unittest

from app.lib.xslt_transformations import apply_xslt
from lxml import html


class ContentParserTestCase(unittest.TestCase):
    def test_RoyalMarines(self):
        # D7829042
        source = '<emph altrender="doctype">RM</emph><persname><emph altrender="surname">Hillyard</emph><emph altrender="forenames">Ernest Percy</emph></persname><emph altrender="num">21311</emph><emph altrender="division">Royal Marine Light Infantry: Plymouth Division</emph><emph altrender="date2">01 October 1918</emph><emph altrender="dob">09 October 1900</emph>'
        schema = "RoyalMarines"
        self.assertEqual(
            """<dl class="tna-dl tna-dl--plain tna-dl--dotted">
<dt>Name</dt>
<dd>Hillyard, Ernest Percy</dd>
<dt>Register number</dt>
<dd>21311</dd>
<dt>Division</dt>
<dd>Royal Marine Light Infantry: Plymouth Division</dd>
<dt>When enlisted/date of enlistment</dt>
<dd>01 October 1918</dd>
<dt>Date of birth</dt>
<dd>09 October 1900</dd>
</dl>
""",
            str(apply_xslt(source, schema)),
        )

    def test_ignored_transformation(self):
        # C11536911
        source = '<span class="wrapper"><span altrender="doctype" class="emph"></span>Joint meeting of the Army-Navy Communication Intelligence Board and Army-Navy Communication Intelligence Co-ordinating Committee, 29 October 1945</span>'
        schema = "Miscellaneous"
        self.assertEqual(
            '<span class="wrapper"><span altrender="doctype" class="emph"></span>Joint meeting of the Army-Navy Communication Intelligence Board and Army-Navy Communication Intelligence Co-ordinating Committee, 29 October 1945</span>',
            str(apply_xslt(source, schema)),
        )
