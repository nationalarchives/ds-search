<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
	</xsl:template>

	<!-- ignore 'doctype' text (should be 'S') -->
	<xsl:template mode="seamenmedal" match="emph[@altrender='doctype']">
	</xsl:template>

	<!-- Display lastname, firstname -->
	<xsl:template mode="seamenmedal" match="persname">
		<tr class="medalRow">
			<td class="medalplain" width="35%"><xsl:text disable-output-escaping="yes">Medal&amp;nbsp;listing&amp;nbsp;of&amp;nbsp;</xsl:text></td>
			<td class="medalplain"><xsl:value-of select="emph[@altrender='surname']/text()"/>
			<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
				<xsl:text disable-output-escaping="yes">, </xsl:text>
			</xsl:if>
			<xsl:value-of select="emph[@altrender='forenames']/text()"/></td>
		</tr>
	</xsl:template>


	<!-- add  dischargeno -->
	<xsl:template mode="seamenmedal" match="emph[@altrender='dischargeno']">
			<tr class="medalRow">
				<td class="medalheader">Discharge number:</td>
				<td class="medalplain"><xsl:value-of select="text()"/>
				</td></tr>
	</xsl:template>

	<!-- add  name of place -->
	<xsl:template mode="seamenmedal" match="geogname">
			<tr class="medalRow">
				<td class="medalheader"> Place of Birth: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>
  
  <!-- add Date of Birth -->
  <xsl:template mode="seamenmedal" match="emph[@altrender='dob']">
    <tr class="medalRow">
      <td class="medalheader"> Date of Birth: </td>
      <td class="medalplain">
        <xsl:value-of select="text()" />
      </td>
    </tr>
  </xsl:template>
  
</xsl:stylesheet>
