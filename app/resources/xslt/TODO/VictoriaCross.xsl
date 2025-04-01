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
  <!-- ignore 'doctype' text (should be 'V') -->
  <xsl:template match="emph[@altrender='doctype']">
		</xsl:template>
  <!-- Display lastname, firstname -->
  <xsl:template match="persname">
    <tr class="medalRow">
      <td class="medalplain" width="35%">
        <xsl:text disable-output-escaping="yes">Victoria&amp;nbsp;Cross&amp;nbsp;details&amp;nbsp;of&amp;nbsp;</xsl:text>
      </td>
      <td class="medalplain">
        <xsl:value-of select="emph[@altrender='surname']/text()"/>
        <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
          <xsl:text disable-output-escaping="yes">, </xsl:text>
        </xsl:if>
        <xsl:value-of select="emph[@altrender='forenames']/text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Rank -->
  <xsl:template match="emph[@altrender='rank']">
    <tr class="medalRow">
      <td class="medalheader"> Rank: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Corps -->
  <xsl:template match="corpname">
    <tr class="medalRow">
      <td class="medalheader"> Regiment: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Date -->
  <xsl:template match="emph[@altrender='date']">
    <tr class="medalRow">
      <td class="medalheader"> Date of Act Of Bravery: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Campaign -->
  <xsl:template match="emph[@altrender='campaign']">
    <tr class="medalRow">
      <td class="medalheader"> Campaign: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Corps -->
  <xsl:template match="geogname">
    <tr class="medalRow">
      <td class="medalheader"> Locale: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
