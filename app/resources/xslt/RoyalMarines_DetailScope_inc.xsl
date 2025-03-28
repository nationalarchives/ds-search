<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	RoyalMarines_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.

    ORIGINAL: https://github.com/nationalarchives/discovery/blob/master/RDWeb/Helpers/XSLs/DoLStyles/RoyalMarines_DetailScope_inc.xsl
		-->
  </xsl:template>

	<xsl:template match="span[@class='emph' and @altrender='doctype']">
	</xsl:template>

	<xsl:template match="/">
    <dl class="tna-dl">
      <xsl:apply-templates/>
    </dl>
	</xsl:template>

  <!-- Display lastname, firstname -->
  <xsl:template match="span[@class='persname']">
    <dt>
      <xsl:text disable-output-escaping="yes">Name</xsl:text>
    </dt>
    <dd>
      <xsl:value-of select="span[@class='emph' and @altrender='surname']/text()"/>
      <xsl:if test="span[@class='emph' and @altrender='surname'] and span[@class='emph' and @altrender='forenames']">
        <xsl:text disable-output-escaping="yes">, </xsl:text>
      </xsl:if>
      <xsl:value-of select="span[@class='emph' and @altrender='forenames']/text()"/>
    </dd>
  </xsl:template>

  <!-- add  age -->
  <xsl:template match="span[@class='emph' and @altrender='num']">
    <dt>Register number</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>

  <!-- add  age -->
  <xsl:template match="span[@class='emph' and @altrender='division']">
    <dt>Division</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>

  <!-- add  age -->
  <xsl:template match="span[@class='emph' and @altrender='dob']">
    <dt>Date of birth</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>

  <!-- add  age -->
  <xsl:template match="span[@class='emph' and @altrender='date2']">
    <dt>When enlisted/date of enlistment</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>

  <!-- add Date of Birth -->
  <xsl:template match="span[@class='emph' and @altrender='dob']">
    <dt>Date of birth</dt>
    <dd>
      <xsl:value-of select="text()"/>
    </dd>
  </xsl:template>
</xsl:stylesheet>