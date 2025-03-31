<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	RNOfficer_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'RN') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <!-- Display lastname, firstname -->
  <xsl:template match="persname">
    <tr class="medalRow">
      <td class="medalplain" width="20%">
        <xsl:text disable-output-escaping="yes">Name </xsl:text>
      </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="emph[@altrender='surname']/text()"/>
        <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
          <xsl:text disable-output-escaping="yes">, </xsl:text>
        </xsl:if>
        <xsl:value-of select="emph[@altrender='forenames']/text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add  age -->
  <xsl:template match="emph[@altrender='rank']">
    <tr class="medalRow">
      <td class="medalheader" width="20%"> Date of Birth: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add  age -->
  <xsl:template match="emph[@altrender='date']">
    <tr class="medalRow">
      <td class="medalheader" width="20%"> Rank: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Date of Birth -->
  <xsl:template match="emph[@altrender='doe']">
    <tr class="medalRow">
      <td class="medalheader"> Date of Appointment: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
