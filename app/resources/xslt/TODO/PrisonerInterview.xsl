<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		###	VERSION: 1.1 	AUTHOR: MHILLYARD	DATE: 23/03/2006
		Modified.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'I') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <!-- Display lastname, firstname -->
  <xsl:template match="persname">
    <tr class="medalRow">
      <td class="medalplain" width="25%">
        <xsl:text disable-output-escaping="yes">Name(s): </xsl:text>
      </td>
      <td class="medalplain" width="35%">
        <xsl:value-of select="emph[@altrender='surname']/text()"/>
        <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
          <xsl:text disable-output-escaping="yes">, </xsl:text>
        </xsl:if>
        <xsl:value-of select="emph[@altrender='forenames']/text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add page -->
  <xsl:template match="emph[@altrender='page']">
    <tr class="medalRow">
      <td class="medalheader"> Page no: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Corps -->
  <xsl:template match="corpname">
    <tr class="medalRow">
      <td class="medalheader"> Corps: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
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
  <!-- add Regiment No -->
  <xsl:template match="emph[@altrender='regno']">
    <tr class="medalRow">
      <td class="medalheader"> Regiment No: </td>
      <td class="medalplain">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add People mentioned -->
  <xsl:template match="emph[@altrender='people']">
    <tr class="medalRow">
      <td class="medalheader"> People mentioned: </td>
      <td class="medalplain">
        <xsl:for-each select="./persname">
          <xsl:value-of select="text()"/>
          <xsl:if test="following-sibling::persname">
            <xsl:text disable-output-escaping="yes">; </xsl:text>
          </xsl:if>
        </xsl:for-each>
      </td>
    </tr>
  </xsl:template>
  <!-- add organisations mentioned -->
  <xsl:template match="emph[@altrender='orgsmentioned']">
    <tr class="medalRow">
      <td class="medalheader"> Organisations mentioned: </td>
      <td class="medalplain">
        <xsl:for-each select="./corpname">
          <xsl:value-of select="text()"/>
          <xsl:if test="following-sibling::corpname">
            <xsl:text disable-output-escaping="yes">; </xsl:text>
          </xsl:if>
        </xsl:for-each>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
