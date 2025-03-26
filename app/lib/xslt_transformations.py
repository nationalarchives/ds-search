import logging

from lxml import etree, html

SCHEMAS = {
    "RoyalMarines": "app/resources/xslt/RoyalMarines_DetailScope_inc.xsl"
}

# Temporary list of schemas to implement - this list will be removed once all schemas are implemented
SCHEMAS_TO_IMPLEMENT = [
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

# These schemas have no known transformation
IGNORE_SCHEMAS = [
    "ANLists",
    "APS",
    "AncestorsMagazine",
    "Datasets",
    "DixonScott",
    "EdenPaper",
    "FOI",
    "IrishMaps",
    "MRR",
    "MapPicture",
    "Miscellaneous",
    "NavyList",
    "Opening2002",
    "Opening2003Defe4",
    "Opening2003Defe5",
    "Opening2003",
    "Opening2006Prem16",
    "Opening2007Prem16",
    "Opening2008Prem16",
    "PrimeMin",
    "RoyalChelsea",
    "SecurityServiceKV",
    "SecurityService",
    "ShipsExploration",
]

logger = logging.getLogger(__name__)


def apply_xslt(html_source, schema):
    if schema in IGNORE_SCHEMAS:
        return html_source
    dom = html.fromstring(html_source)
    try:
        schema_xslt = SCHEMAS[schema]
    except KeyError:
        # Temporary check to avoid errors while implementing all schemas
        if schema not in SCHEMAS_TO_IMPLEMENT:
            logger.error(f"Schema '{schema}' not found")
        return html_source
    xslt = etree.parse(schema_xslt)
    transform = etree.XSLT(xslt)
    result = transform(dom)
    return result
