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
  <!-- ignore 'doctype' text (should be 'R') -->
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
  <!-- add Official Number -->
  <xsl:template match="emph[@altrender='num']">
    <dt>Official number</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Official Number -->
  <xsl:template match="emph[@altrender='num2']">
    <dt>Continuous service number</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add  Date of birth -->
  <xsl:template match="emph[@altrender='age']">
    <dt>Date of birth</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add  Date of Volunteering -->
  <xsl:template match="emph[@altrender='date']">
    <dt>Date of volunteering</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add  place of birth -->
  <xsl:template match="geogname">
    <dt>Place of birth</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Rank -->
  <xsl:template match="emph[@altrender='rank']">
    <dt>RNVR division</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Date of Birth -->
  <xsl:template match="emph[@altrender='dob']">
    <dt>Date of birth</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
  <!-- add Comments-->
  <xsl:template match="emph[@altrender='comments']">
    <dt>Comments</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
</xsl:stylesheet>