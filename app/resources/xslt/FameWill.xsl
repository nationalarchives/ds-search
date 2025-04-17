<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="emph[@altrender='doctype']">
  </xsl:template>
  <xsl:template match="emph[@altrender='perstitle']">
    <xsl:value-of select="text()"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="persname">
    <xsl:value-of select="emph[@altrender='forenames']/text()"/>
    <xsl:if test="emph[@altrender='surname']">
      <xsl:text disable-output-escaping="yes"> </xsl:text>
      <xsl:value-of select="emph[@altrender='surname']/text()"/>
    </xsl:if>
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="text()">
    <xsl:call-template name="replace">
      <xsl:with-param name="string" select="."/>
    </xsl:call-template>
  </xsl:template>
  <xsl:template name="replace">
    <xsl:param name="string"/>
    <xsl:choose>
      <xsl:when test="contains($string,'&#10;')">
        <xsl:value-of select="substring-before($string,'&#10;')"/>
        <br/>
        <xsl:call-template name="replace">
          <xsl:with-param name="string" select="substring-after($string,'&#10;')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$string"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
