import unittest

from app.lib.xslt_transformations import apply_xslt


class ContentParserTestCase(unittest.TestCase):
    def test_BritishWarMedal(self):
        # D8030479
        source = '<emph altrender="doctype">BW</emph><persname><emph altrender="surname">Hillyard</emph><emph altrender="forenames">Henry William</emph></persname><geogname>Rowhedge</geogname><emph altrender="dob">1873</emph>'
        schema = "BritishWarMedal"
        self.assertEqual(
            """<dl class="tna-dl tna-dl--plain tna-dl--dotted">
<dt>Name</dt>
<dd>Hillyard, Henry William</dd>
<dt>Place of birth</dt>
<dd>Rowhedge</dd>
<dt>Date of birth</dt>
<dd>1873</dd>
</dl>""",
            str(apply_xslt(source, schema)),
        )

    def test_DeathDuty(self):
        # D8030479
        source = '<emph altrender="doctype">A</emph><persname> <emph altrender="forenames">Edmund</emph><emph altrender="surname">Barnes</emph></persname><occupation>Farmer</occupation><geogname>Cringleford, Norfolk</geogname>'
        schema = "DeathDuty"
        self.assertEqual(
            """Abstract of administration of Edmund Barnes, Farmer of Cringleford, Norfolk""",
            str(apply_xslt(source, schema)),
        )

    def test_Medal(self):
        # D2874592
        source = '<emph altrender="doctype">M</emph><persname><emph altrender="surname">Hillyard</emph> <emph altrender="forenames">Ernest S</emph></persname><emph altrender="medal"><corpname>Northamptonshire Regiment</corpname><emph altrender="regno">9004</emph><emph altrender="rank">Driver</emph></emph><emph altrender="medal"><corpname>Northamptonshire Regiment</corpname><emph altrender="regno">9004</emph><emph altrender="rank">Private</emph></emph><emph altrender="medal"><corpname>Northamptonshire Regiment</corpname><emph altrender="regno">5875061</emph><emph altrender="rank">Private</emph></emph>'
        schema = "Medal"
        self.assertEqual(
            """<div class="tna-table-wrapper"><table class="tna-table">
<caption class="tna-table__caption">Medal card of Hillyard, Ernest S</caption>
<thead class="tna-table__head"><tr class="tna-table__row">
<th scope="col" class="tna-table__header">Corps</th>
<th scope="col" class="tna-table__header">Regiment number</th>
<th scope="col" class="tna-table__header">Rank</th>
</tr></thead>
<tbody class="tna-table__body">
<tr class="tna-table__row">
<th class="tna-table__header" scope="row">Northamptonshire Regiment</th>
<td class="tna-table__cell">9004</td>
<td class="tna-table__cell">Driver</td>
</tr>
<tr class="tna-table__row">
<th class="tna-table__header" scope="row">Northamptonshire Regiment</th>
<td class="tna-table__cell">9004</td>
<td class="tna-table__cell">Private</td>
</tr>
<tr class="tna-table__row">
<th class="tna-table__header" scope="row">Northamptonshire Regiment</th>
<td class="tna-table__cell">5875061</td>
<td class="tna-table__cell">Private</td>
</tr>
</tbody>
</table></div>""",
            str(apply_xslt(source, schema)),
        )

    def test_NavalReserve(self):
        # D8485886
        source = '<emph altrender="doctype">RR</emph><persname><emph altrender="surname">Hillyard</emph><emph altrender="forenames">Edward Joshua</emph></persname><geogname>Rowhedge, Essex</geogname><emph altrender="certno">B 3813</emph><emph altrender="rank"></emph><emph altrender="date"></emph><emph altrender="dob">19 November 1885</emph>'
        schema = "NavalReserve"
        self.assertEqual(
            """<dl class="tna-dl tna-dl--plain tna-dl--dotted">
<dt>Name</dt>
<dd>Hillyard, Edward Joshua</dd>
<dt>Place of birth</dt>
<dd>Rowhedge, Essex</dd>
<dt>Number</dt>
<dd>B 3813</dd>
<dt>Date of birth</dt>
<dd>19 November 1885</dd>
</dl>""",
            str(apply_xslt(source, schema)),
        )

    def test_RAFOfficers(self):
        # D8272609
        source = '<emph altrender="doctype">RO</emph><persname><emph altrender="surname">Hillyard</emph><emph altrender="forenames">Frederick</emph></persname><emph altrender="dob">08 July 1898</emph>'
        schema = "RAFOfficers"
        self.assertEqual(
            """<dl class="tna-dl tna-dl--plain tna-dl--dotted">
<dt>Name</dt>
<dd>Hillyard, Frederick</dd>
<dt>Date of birth</dt>
<dd>08 July 1898</dd>
</dl>""",
            str(apply_xslt(source, schema)),
        )

    def test_RecHonours(self):
        # C9041173
        source = '<emph altrender="doctype">H</emph><persname> <emph altrender="surname">Fetterley</emph><emph altrender="forenames">James</emph></persname><emph altrender="rank">Lieutenant</emph><emph altrender="regno">CDN541</emph><corpname>2 Battalion The East Yorkshire Regiment</corpname><geogname>North West Europe</geogname><emph altrender="award">Military Cross</emph><emph altrender="date">21 December 1944</emph><emph altrender="folio">2-3</emph>'
        schema = "RecHonours"
        self.assertEqual(
            """<dl class="tna-dl tna-dl--plain tna-dl--dotted">
<dt>Name</dt>
<dd>Fetterley, James</dd>
<dt>Rank</dt>
<dd>Lieutenant</dd>
<dt>Service number</dt>
<dd>CDN541</dd>
<dt>Regiment</dt>
<dd>2 Battalion The East Yorkshire Regiment</dd>
<dt>Theatre of combat or operation</dt>
<dd>North West Europe</dd>
<dt>Award</dt>
<dd>Military Cross</dd>
<dt>Date of announcement in London Gazette</dt>
<dd>21 December 1944</dd>
<dt>Folio</dt>
<dd>2-3</dd>
</dl>""",
            str(apply_xslt(source, schema)),
        )

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
</dl>""",
            str(apply_xslt(source, schema)),
        )

    def test_SeamenMedal(self):
        # D4340681
        source = '<emph altrender="doctype">S</emph><persname><emph altrender="surname">Hillyard</emph><emph altrender="forenames">William Henry</emph></persname><emph altrender="dischargeno">R166522</emph><emph altrender="dob">01 September 1919</emph>'
        schema = "SeamenMedal"
        self.assertEqual(
            """<dl class="tna-dl tna-dl--plain tna-dl--dotted">
<dt>Name</dt>
<dd>Hillyard, William Henry</dd>
<dt>Discharge number</dt>
<dd>R166522</dd>
<dt>Date of birth</dt>
<dd>01 September 1919</dd>
</dl>""",
            str(apply_xslt(source, schema)),
        )

    def test_SeamenRegister(self):
        # D7004597
        source = '<emph altrender="doctype">R</emph><persname><emph altrender="surname">Hillyard</emph> <emph altrender="forenames">Ernest Edward</emph></persname><emph altrender="num">K46763</emph><geogname>Luton, Bedfordshire</geogname><emph altrender="dob">24 August 1899</emph>'
        schema = "SeamenRegister"
        self.assertEqual(
            """<dl class="tna-dl tna-dl--plain tna-dl--dotted">
<dt>Name</dt>
<dd>Hillyard, Ernest Edward</dd>
<dt>Official number</dt>
<dd>K46763</dd>
<dt>Place of birth</dt>
<dd>Luton, Bedfordshire</dd>
<dt>Date of birth</dt>
<dd>24 August 1899</dd>
</dl>""",
            str(apply_xslt(source, schema)),
        )

    def test_Will(self):
        # D538741
        source = '<emph altrender="doctype">W</emph><persname><emph altrender="forenames">William</emph><emph altrender="surname">Cribb</emph></persname><occupation>Baker</occupation><geogname>Wareham , Dorset</geogname>'
        schema = "Will"
        self.assertEqual(
            "Will of William Cribb, Baker of Wareham , Dorset",
            str(apply_xslt(source, schema)),
        )

    def test_ignored_transformation(self):
        # C11536911
        source = '<emph altrender="doctype">G</emph>Joint meeting of the Army-Navy Communication Intelligence Board and Army-Navy Communication Intelligence Co-ordinating Committee, 29 October 1945'
        schema = "Miscellaneous"
        self.assertEqual(
            '<emph altrender="doctype">G</emph>Joint meeting of the Army-Navy Communication Intelligence Board and Army-Navy Communication Intelligence Co-ordinating Committee, 29 October 1945',
            str(apply_xslt(source, schema)),
        )
