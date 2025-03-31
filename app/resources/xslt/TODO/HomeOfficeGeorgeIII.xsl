<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
	</xsl:template>

	<!-- ignore 'doctype' text (should be 'DC') -->
	<xsl:template mode="HomeOfficeGeorge" match="emph[@altrender='doctype']">
	</xsl:template>


	<!-- add Scope -->
	<xsl:template mode="HomeOfficeGeorge" match="emph[@altrender='scope']">
	<tr class="medalRow">
	<td class="medalheader" width="10%"><xsl:text disable-output-escaping="yes">Content: </xsl:text> </td>
	<td class="medalplain" width="90%"><xsl:value-of disable-output-escaping="yes" select="text()" />
	</td></tr>
	</xsl:template>
	
</xsl:stylesheet>

