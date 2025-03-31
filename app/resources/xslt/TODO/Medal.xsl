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
	<xsl:template mode="medal" match="emph[@altrender='doctype']">
	</xsl:template>

	<!-- Display lastname, firstname -->
	<xsl:template mode="medal" match="persname">
		<tr>	
			<td colspan="2" class="medalplain"><xsl:text>Medal card of </xsl:text>
			<xsl:value-of select="emph[@altrender='surname']/text()"/>
			<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
				<xsl:text disable-output-escaping="yes">, </xsl:text>
			</xsl:if>
			<xsl:value-of select="emph[@altrender='forenames']/text()"/></td>
		</tr>
	</xsl:template>

	<!-- Display details of all regiments -->
	<xsl:template mode="medal" match="emph[@altrender='medal']">
		
		<!-- show heading row for regiment details columns -->
		<xsl:if test="count(preceding-sibling::emph[@altrender='medal']) = 0">
			<tr class="medalHeaderDetail"><th width="33%" scope="col" class="medalplain">Corps</th><th width="33%" scope="col" class="medalplain">Regiment No</th><th width="33%" scope="col" class="medalplain">Rank</th></tr>
		</xsl:if>
		
		<tr valign="top">
		<!-- show regiment name in first column -->
		<td class="medalplain"><xsl:if test="corpname">
			<xsl:value-of select="corpname/text()"/>
		</xsl:if></td>
		
		<!-- show regiment number in second column -->
		<td class="medalplain"><xsl:if test="emph[@altrender='regno']">
			<xsl:value-of select="emph[@altrender='regno']/text()"/>
		</xsl:if></td>
		
		<!-- show rank in third column -->
		<td class="medalplain"><xsl:if test="emph[@altrender='rank']">
			<xsl:value-of select="emph[@altrender='rank']/text()"/>
		</xsl:if></td>
		</tr>
	</xsl:template>

</xsl:stylesheet>
