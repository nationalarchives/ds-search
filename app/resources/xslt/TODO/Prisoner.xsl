<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
	</xsl:template>

	<!-- ignore 'doctype' text (should be 'P') -->
	<xsl:template mode="prisoner" match="emph[@altrender='doctype']">
	</xsl:template>

	<!-- Display lastname, firstname -->
	<xsl:template mode="prisoner" match="persname">
		<tr class="medalRow">
			<td class="medalplain"><xsl:text disable-output-escaping="yes">Name (and alias if used) of prisoner</xsl:text></td>
			<td class="medalplain"><xsl:value-of select="emph[@altrender='surname']/text()"/>
			<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
				<xsl:text disable-output-escaping="yes">, </xsl:text>
			</xsl:if>
			<xsl:value-of select="emph[@altrender='forenames']/text()"/></td>
		</tr>
	</xsl:template>


	<!-- add  name of place -->
	<xsl:template mode="prisoner" match="geogname">
			<tr class="medalRow">
				<td class="medalheader" width="30%"> Place of Birth: </td>
				<td class="medalplain" width="60%"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>

	<!-- add  age -->
	<xsl:template mode="prisoner" match="emph[@altrender='age']">
			<tr class="medalRow">
				<td class="medalheader"> Age: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>



	<!-- add  court -->
	<xsl:template mode="prisoner" match="emph[@altrender='court']">
			<tr class="medalRow">
				<td class="medalheader"> Place/Court of conviction: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>

	<!-- add  offence -->
	<xsl:template mode="prisoner" match="emph[@altrender='offence']">
			<tr class="medalRow">
				<td class="medalheader"> Offence: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>

	<!-- add  sentence -->
	<xsl:template mode="prisoner" match="emph[@altrender='sentence']">
			<tr class="medalRow">
				<td class="medalheader"> Sentence: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>


</xsl:stylesheet>
