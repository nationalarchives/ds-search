import logging

from lxml import etree, html

SCHEMAS = {
    "RoyalMarines": "app/resources/xslt/RoyalMarines_DetailScope_inc.xsl"
}

logger = logging.getLogger(__name__)


def apply_xslt(html_source, schema):
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
