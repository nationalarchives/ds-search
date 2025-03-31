<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	ShippingSeamen_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'SS') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <!-- Display Ship Name -->
  <xsl:template match="emph[@altrender='name']">
    <tr class="medalRow">
      <td class="medalheader" width="20%"> Ship Name: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- Display Ship Name -->
  <xsl:template match="emph[@altrender='name2']">
    <tr class="medalRow">
      <td class="medalheader" width="20%"> Former Ship Name: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add  age -->
  <xsl:template match="emph[@altrender='size']">
    <tr class="medalRow">
      <td class="medalheader" width="20%"> Gross Tonnage: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Corps -->
  <xsl:template match="geogname">
    <tr class="medalRow">
      <td class="medalheader"> Country of Origin: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add  age -->
  <xsl:template match="emph[@altrender='card']">
    <tr class="medalRow">
      <td class="medalheader" width="20%"> Type of Card: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
