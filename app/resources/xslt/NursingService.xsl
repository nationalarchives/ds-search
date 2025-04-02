<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <xsl:template match="persname">
    <xsl:value-of select="emph[@altrender='surname']/text()"/>
    <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <xsl:value-of select="emph[@altrender='forenames']/text()"/>
  </xsl:template>
</xsl:stylesheet>
