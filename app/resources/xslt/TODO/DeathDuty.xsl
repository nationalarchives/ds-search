<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	Will_DetailScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: RBEASLEY	DATE: 10/10/2003
		Created.
		-->
  </xsl:template>
  <!-- write 'doctype' static text depending on value -->
  <xsl:template match="emph[@altrender='doctype']">
    <xsl:choose>
      <xsl:when test="text()='W'">
        <xsl:text>Abstract of Will of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='A'">
        <xsl:text>Abstract of Administration of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='W '">
        <xsl:text>Abstract of Will of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='A '">
        <xsl:text>Abstract of Administration of </xsl:text>
      </xsl:when>
    </xsl:choose>
  </xsl:template>
  <!-- show title and " "-->
  <xsl:template match="emph[@altrender='perstitle']">
    <xsl:value-of select="text()"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <!-- show firstname " " lastname -->
  <xsl:template match="persname">
    <xsl:value-of select="emph[@altrender='forenames']/text()"/>
    <xsl:if test="emph[@altrender='surname']">
      <xsl:text disable-output-escaping="yes"> </xsl:text>
      <xsl:value-of select="emph[@altrender='surname']/text()"/>
    </xsl:if>
  </xsl:template>
  <!-- add ", " then occupation -->
  <xsl:template match="occupation">
    <xsl:text>, </xsl:text>
    <xsl:value-of select="text()"/>
  </xsl:template>
  <!-- add " of " then name of place -->
  <xsl:template match="geogname">
    <xsl:text> of </xsl:text>
    <xsl:value-of select="text()"/>
  </xsl:template>
</xsl:stylesheet>
