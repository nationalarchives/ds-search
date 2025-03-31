<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
	</xsl:template>

	<!-- ignore 'doctype' text (should be 'OL') -->
	<xsl:template mode="Olympic" match="emph[@altrender='doctype']">
	</xsl:template>

	<!-- add Place -->
	<xsl:template mode="Olympic" match="geogname">
			<tr class="medalRow">
			<td class="medalplain"> Place: </td>
			<td class="medalplain"><xsl:value-of select="text()" />
		</td></tr>
	</xsl:template>	
	
	<!-- add Scope and Content -->
	<xsl:template mode="Olympic" match="emph[@altrender='scope']">
	<tr class="medalRow">
		<td class="medalplain" width="30%"><xsl:text disable-output-escaping="yes"> Scope and Content:  </xsl:text> </td>
		<td class="medalplain" width="60%"><xsl:value-of disable-output-escaping="yes" select="text()" />
	</td></tr>
	</xsl:template>	
	
</xsl:stylesheet>

