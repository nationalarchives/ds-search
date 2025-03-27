import unittest

from app.lib.xslt_transformations import apply_xslt
from lxml import html


class ContentParserTestCase(unittest.TestCase):
    def test_RoyalMarines(self):
        # D7829042
        source = '<span class="wrapper"><span altrender="doctype" class="emph"></span><span class="persname"><span altrender="surname" class="emph">Hillyard</span><span altrender="forenames" class="emph">Ernest Percy</span></span><span altrender="num" class="emph">21311</span><span altrender="division" class="emph">Royal Marine Light Infantry: Plymouth Division</span><span altrender="date2" class="emph">01 October 1918</span><span altrender="dob" class="emph">09 October 1900</span></span>'
        schema = "RoyalMarines"
        self.assertEqual(
            """<dl class="tna-dl">
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
