<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <xsl:template match="emph[@altrender='scope']">
    <xsl:value-of select="text()"/>
  </xsl:template>
</xsl:stylesheet>
