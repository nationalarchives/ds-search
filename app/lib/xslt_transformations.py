import logging

from lxml import etree, html

SCHEMAS = {
    "Airwomen": "Airwomen.xsl",
    "AliensRegCards": "AliensRegCards.xsl",
    "AncientPetitions": "AncientPetitions.xsl",
    "BritishWarMedal": "BritishWarMedal.xsl",
    "CabinetPapers": "CabinetPapers.xsl",
    "CombatRepWW2": "CombatRepWW2.xsl",
    "DeathDuty": "DeathDuty.xsl",
    "DNPC": "DNPC.xsl",
    "DomesdayBook": "DomesdayBook.xsl",
    "EffectsPapers": "EffectsPapers.xsl",
    "FameWill": "FameWill.xsl",
    "GallantrySea": "GallantrySea.xsl",
    "LootedArt": "LootedArt.xsl",
    "Medal": "Medal.xsl",
    "Miscellaneous": "Miscellaneous.xsl",
    "MusterRolls": "MusterRolls.xsl",
    "NavalOfficers": "NavalOfficers.xsl",
    "NavalReserve": "NavalReserve.xsl",
    "NavyLandService": "NavyLandService.xsl",
    "NursingService": "NursingService.xsl",
    "Olympic": "Olympic.xsl",
    "PoorLaw": "PoorLaw.xsl",
    "prisoner": "prisoner.xsl",
    "PrisonerInterview": "PrisonerInterview.xsl",
    "RAFOfficers": "RAFOfficers.xsl",
    "RecHonours": "RecHonours.xsl",
    "RNASOfficers": "RNASOfficers.xsl",
    "RNOfficer": "RNOfficer.xsl",
    "RoyalMarines": "RoyalMarines.xsl",
    "SeamenMedal": "SeamenMedal.xsl",
    "SeamenRegister": "SeamenRegister.xsl",
    "SeamenWill": "SeamenWill.xsl",
    "ShippingSeamen": "ShippingSeamen.xsl",
    "Squadron": "Squadron.xsl",
    "Titanic": "Titanic.xsl",
    "VictoriaCross": "VictoriaCross.xsl",
    "VolunteerReserve": "VolunteerReserve.xsl",
    "Will": "Will.xsl",
    "WomensCorps": "WomensCorps.xsl",
    "Wrns": "Wrns.xsl",
}

logger = logging.getLogger(__name__)


def apply_xslt(html_source: str, schema: str) -> str:
    dom = html.fromstring(html_source)
    schema_xslt = SCHEMAS.get(schema, "Miscellaneous.xsl")
    try:
        xslt = etree.parse(f"app/resources/xslt/{schema_xslt}")
    except Exception as e:
        logger.error(
            f"Unexpected error while loading XSLT file '{schema_xslt}': {e}"
        )
        return html_source
    transform = etree.XSLT(xslt)
    result = transform(dom)
    return str(result).strip()
