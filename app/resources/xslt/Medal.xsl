<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	Medal_DetailScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.1 	AUTHOR: RBEASLEY	DATE: 27/11/2003
		Altered test for displaying the first medal to test that there is
		no previous medals rather than test the node value matches the first
		medal value (fix for two medals with same values)

		###	VERSION: 1.0 	AUTHOR: RBEASLEY	DATE: 10/10/2003
		Created.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'M') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <!-- Display the table -->
  <xsl:template match="/">
    <div class="tna-table-wrapper">
      <table class="tna-table">
        <xsl:apply-templates select="node()/persname"/>
        <thead class="tna-table__head">
          <tr class="tna-table__row">
            <th scope="col" class="tna-table__header">Corps</th>
            <th scope="col" class="tna-table__header">Regiment number</th>
            <th scope="col" class="tna-table__header">Rank</th>
          </tr>
        </thead>
        <tbody class="tna-table__body">
          <xsl:apply-templates select="node()/emph[@altrender='medal']"/>
        </tbody>
      </table>
    </div>
  </xsl:template>
  <!-- Display details of the person -->
  <xsl:template match="persname">
    <caption class="tna-table__caption">
      <xsl:text>Medal card of </xsl:text>
      <xsl:value-of select="emph[@altrender='surname']/text()"/>
      <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
        <xsl:text disable-output-escaping="yes">, </xsl:text>
      </xsl:if>
      <xsl:value-of select="emph[@altrender='forenames']/text()"/>
    </caption>
  </xsl:template>
  <!-- Display details of all regiments -->
  <xsl:template match="emph[@altrender='medal']">
    <tr class="tna-table__row">
      <!-- show regiment name in first column -->
      <th class="tna-table__header" scope="row">
        <xsl:if test="corpname">
          <xsl:value-of select="corpname/text()"/>
        </xsl:if>
      </th>
      <!-- show regiment number in second column -->
      <td class="tna-table__cell">
        <xsl:if test="emph[@altrender='regno']">
          <xsl:value-of select="emph[@altrender='regno']/text()"/>
        </xsl:if>
      </td>
      <!-- show rank in third column -->
      <td class="tna-table__cell">
        <xsl:if test="emph[@altrender='rank']">
          <xsl:value-of select="emph[@altrender='rank']/text()"/>
        </xsl:if>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
