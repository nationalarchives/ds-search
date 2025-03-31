<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="emph[@altrender='doctype']">
    <xsl:choose>
      <xsl:when test="text()='W'">
        <xsl:text>Will of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='S'">
        <xsl:text>Sentence of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='W '">
        <xsl:text>Will of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='S '">
        <xsl:text>Sentence of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='IW'">
        <xsl:text>Incomplete will of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='UW'">
        <xsl:text>Unfinished will of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='US'">
        <xsl:text>Unfinished sentence of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='IS'">
        <xsl:text>Incomplete sentence of </xsl:text>
      </xsl:when>
      <xsl:when test="text()='WS'">
        <xsl:text>Will and sentence of </xsl:text>
      </xsl:when>
    </xsl:choose>
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
  </xsl:template>
  <xsl:template match="occupation">
    <xsl:text>, </xsl:text>
    <xsl:value-of select="text()"/>
  </xsl:template>
  <xsl:template match="geogname">
    <xsl:text> of </xsl:text>
    <xsl:value-of select="text()"/>
  </xsl:template>
</xsl:stylesheet>
