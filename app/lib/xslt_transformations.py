import logging

from lxml import etree, html

SCHEMAS = {
    "BritishWarMedal": "BritishWarMedal.xsl",
    "DeathDuty": "DeathDuty.xsl",
    "Medal": "Medal.xsl",
    "NavalReserve": "RoyalNavalReserve.xsl",
    "RAFOfficers": "RAFOfficers.xsl",
    "RecHonours": "RecHonours.xsl",
    "RNOfficer": "RNOfficer.xsl",
    "RoyalMarines": "RoyalMarines.xsl",
    "SeamenMedal": "SeamenMedal.xsl",
    "SeamenRegister": "RegSea.xsl",
    "Will": "Will.xsl",
}

# Temporary list of schemas to implement - this list will be removed once all schemas are implemented
SCHEMAS_TO_IMPLEMENT = [
    "Airwomen",
    "AliensRegCards",
    "AncientPetitions",
    "CabinetPapers",
    "CombatRepWW2",
    "DNPC",
    "DomesdayBook",
    "EffectsPapers",
    "FameWill",
    "GallantrySea",
    "LootedArt",
    "MusterRolls",
    "NavalOfficers",
    "NavyLandService",
    "NursingService",
    "Olympic",
    "PoorLaw",
    "prisoner",
    "PrisonerInterview",
    "RNASOfficers",
    "SeamenWill",
    "ShippingSeamen",
    "Squadron",
    "Titanic",
    "VictoriaCross",
    "VolunteerReserve",
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


def apply_xslt(html_source: str, schema: str) -> str:
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
