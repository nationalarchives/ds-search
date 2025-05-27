<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
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
  <xsl:template match="persname">
    <caption class="tna-table__caption">
      <xsl:text>Medal card of </xsl:text>
      <xsl:value-of select="emph[@altrender='surname']/text()"/>
      <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="emph[@altrender='forenames']/text()"/>
    </caption>
  </xsl:template>
  <xsl:template match="emph[@altrender='medal']">
    <tr class="tna-table__row">
      <th class="tna-table__header" scope="row">
        <xsl:if test="corpname">
          <xsl:value-of select="corpname/text()"/>
        </xsl:if>
      </th>
      <td class="tna-table__cell">
        <xsl:if test="emph[@altrender='regno']">
          <xsl:value-of select="emph[@altrender='regno']/text()"/>
        </xsl:if>
      </td>
      <td class="tna-table__cell">
        <xsl:if test="emph[@altrender='rank']">
          <xsl:value-of select="emph[@altrender='rank']/text()"/>
        </xsl:if>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
