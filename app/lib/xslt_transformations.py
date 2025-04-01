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
    "NavalReserve": "NavalReserve.xsl",
    "NavyLandService": "NavyLandService.xsl",
    "RAFOfficers": "RAFOfficers.xsl",
    "RecHonours": "RecHonours.xsl",
    "RNOfficer": "RNOfficer.xsl",
    "RoyalMarines": "RoyalMarines.xsl",
    "SeamenMedal": "SeamenMedal.xsl",
    "SeamenRegister": "SeamenRegister.xsl",
    "VolunteerReserve": "VolunteerReserve.xsl",
    "Will": "Will.xsl",
}

# Temporary list of schemas to implement - this list will be removed once all schemas are implemented
SCHEMAS_TO_IMPLEMENT = [
    "MusterRolls",
    "NavalOfficers",
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
