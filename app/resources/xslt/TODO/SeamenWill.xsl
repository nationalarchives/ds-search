<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	SeamenWill_DetailedScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		###	VERSION: 1.1 	AUTHOR: MHILLYARD	DATE: 30/08/2007
		Modified.
		-->
  </xsl:template>
  <!-- write 'doctype' static text depending on value -->
  <xsl:template match="emph[@altrender='doctype']">
    <!--tr class="medalRow"-->
    <td class="medalplain" width="20%">
      <xsl:choose>
        <xsl:when test="text()='W'">
          <xsl:text>Will of </xsl:text>
        </xsl:when>
        <xsl:when test="text()='P'">
          <xsl:text>Papers relating to </xsl:text>
        </xsl:when>
      </xsl:choose>
    </td>
    <!--td class="medalplain">
		<xsl:value-of select="emph[@altrender='surname']/text()"/>
			<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
		<xsl:text disable-output-escaping="yes">, </xsl:text>
		</xsl:if>
		<xsl:value-of select="emph[@altrender='forenames']/text()"/>
	</td-->
    <!--/tr-->
  </xsl:template>
  <!-- show title and " "-->
  <xsl:template match="persname">
    <!--tr class="medalRow"-->
    <!--td class="medalplain"></td-->
    <td class="medalplain" width="20%">
      <xsl:value-of select="emph[@altrender='surname']/text()"/>
      <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
        <xsl:text disable-output-escaping="yes">, </xsl:text>
      </xsl:if>
      <xsl:value-of select="emph[@altrender='forenames']/text()"/>
    </td>
    <!--/tr-->
  </xsl:template>
  <!-- add Rank -->
  <xsl:template match="emph[@altrender='rank']">
    <tr class="medalRow">
      <td class="medalplain" width="20%"> Rank/Rating: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Ship Name -->
  <xsl:template match="corpname">
    <tr class="medalRow">
      <td class="medalplain" width="20%"> Ship Name: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Ship's paybook number -->
  <xsl:template match="emph[@altrender='num']">
    <tr class="medalRow">
      <td class="medalplain" width="20%"> Ship's Pay Book number: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Date of will -->
  <xsl:template match="emph[@altrender='date']">
    <tr class="medalRow">
      <td class="medalplain" width="20%">  Date of Will: </td>
      <td class="medalplain" width="20%">
        <xsl:value-of select="text()"/>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
