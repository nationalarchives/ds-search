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

SERIES_TRANSFORMATIONS = {
    "ADM 240": "ADM_240.xsl",
    "DL 25": "DL_25.xsl",
}


logger = logging.getLogger(__name__)


def xsl_transformation(source: str, schema_file: str) -> str:
    dom = html.fromstring(source)
    try:
        xslt = etree.parse(f"app/resources/xslt/{schema_file}")
    except Exception as e:
        logger.error(
            f"Unexpected error while loading XSLT file '{schema_file}': {e}"
        )
        return source
    transform = etree.XSLT(xslt)
    result = transform(dom)
    return str(result).strip()


def apply_schema_xsl(source: str, schema: str) -> str:
    schema_xslt = SCHEMAS.get(schema, "Miscellaneous.xsl")
    return xsl_transformation(source, schema_xslt)


def apply_series_xsl(source: str, division: str) -> str:
    if schema := SERIES_TRANSFORMATIONS.get(division):
        return xsl_transformation(source, schema)
    return source
