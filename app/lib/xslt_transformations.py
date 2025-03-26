import logging

from lxml import etree, html

SCHEMAS = {
    "RoyalMarines": "app/resources/xslt/RoyalMarines_DetailScope_inc.xsl"
}

IGNORE_SCHEMAS = [
    "default",
    "Airwomen",
    "AliensRegCards",
    "AncientPetitions",
    "BritishWarMedal",
    "CabinetPapers",
    "CombatRepWW2",
    "DNPC",
    "DeathDuty",
    "DomesdayBook",
    "EffectsPapers",
    "FameWill",
    "GallantrySea",
    "LootedArt",
    "Medal",
    "Miscellaneous",
    "MusterRolls",
    "NavalOfficers",
    "NavalReserve",
    "NavyLandService",
    "NursingService",
    "Olympic",
    "PoorLaw",
    "prisoner",
    "PrisonerInterview",
    "RAFOfficers",
    "RNASOfficers",
    "RNOfficer",
    "RecHonours",
    "SeamenMedal",
    "SeamenRegister",
    "SeamenWill",
    "ShippingSeamen",
    "Squadron",
    "Titanic",
    "VictoriaCross",
    "VolunteerReserve",
    "Will",
    "WomensCorps",
    "Wrns",
]


logger = logging.getLogger(__name__)


def apply_xslt(html_source, schema):
    if schema in IGNORE_SCHEMAS:
        return html_source
    dom = html.fromstring(html_source)
    try:
        schema_xslt = SCHEMAS[schema]
    except KeyError:
        logger.error(f"Schema '{schema}' not found")
        return html_source
    xslt = etree.parse(schema_xslt)
    transform = etree.XSLT(xslt)
    result = transform(dom)
    return result
