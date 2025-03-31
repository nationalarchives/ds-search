<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'H') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <xsl:template match="/">
    <dl class="tna-dl tna-dl--plain tna-dl--dotted">
      <xsl:apply-templates/>
    </dl>
  </xsl:template>
  <!-- Display lastname, firstname -->
  <xsl:template match="persname">
    <dt>
      <xsl:text disable-output-escaping="yes">Name</xsl:text>
    </dt>
    <dd>
      <xsl:value-of select="emph[@altrender='surname']/text()"/>
      <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
        <xsl:text disable-output-escaping="yes">, </xsl:text>
      </xsl:if>
      <xsl:value-of select="emph[@altrender='forenames']/text()"/>
    </dd>
  </xsl:template>
  <!-- add Rank -->
  <xsl:template match="emph[@altrender='rank']">
    <dt>Rank</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Regiment No -->
  <xsl:template match="emph[@altrender='regno']">
    <dt>Service number</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Corps -->
  <xsl:template match="corpname">
    <dt>Regiment</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Corps -->
  <xsl:template match="geogname">
    <dt>Theatre of combat or operation</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Regiment No -->
  <xsl:template match="emph[@altrender='award']">
    <dt>Award</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Regiment No -->
  <xsl:template match="emph[@altrender='date']">
    <dt>Date of announcement in London Gazette</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Folio -->
  <xsl:template match="emph[@altrender='folio']">
    <dt>Folio</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
</xsl:stylesheet>
