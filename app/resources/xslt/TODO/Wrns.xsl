<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	Wrns_DetailScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: PDAVIS	DATE: 29/01/2007
		Created.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'WR') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <!-- Display lastname, firstname -->
  <xsl:template match="persname">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes">Service record of </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of select="emph[@altrender='surname']/text()"/>
        <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
          <xsl:text disable-output-escaping="yes">, </xsl:text>
        </xsl:if>
        <xsl:value-of select="emph[@altrender='perstitle']/text()"/>
        <xsl:if test="emph[@altrender='perstitle']">
          <xsl:text disable-output-escaping="yes"> </xsl:text>
        </xsl:if>
        <xsl:value-of select="emph[@altrender='forenames']/text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Ship's paybook number -->
  <xsl:template match="emph[@altrender='num']">
    <tr class="medalRow">
      <td class="medalplain"> Service number: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Date of will -->
  <xsl:template match="emph[@altrender='rank']">
    <tr class="medalRow">
      <td class="medalplain">  Rating: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Date of will -->
  <xsl:template match="emph[@altrender='date']">
    <tr class="medalRow">
      <td class="medalplain">  Date of enrolment: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
