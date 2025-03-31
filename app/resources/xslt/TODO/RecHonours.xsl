<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
	</xsl:template>

	<!-- ignore 'doctype' text (should be 'H') -->
	<xsl:template mode="RecHonours" match="emph[@altrender='doctype']">
	</xsl:template>

	<!-- Display lastname, firstname -->
	<xsl:template mode="RecHonours" match="persname">
		<tr class="medalRow">
			<td class="medalplain" width="30%"><xsl:text disable-output-escaping="yes">Name </xsl:text></td>
			<td class="medalplain" width="60%"><xsl:value-of select="emph[@altrender='surname']/text()"/>
			<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
				<xsl:text disable-output-escaping="yes">, </xsl:text>
			</xsl:if>
			<xsl:value-of select="emph[@altrender='forenames']/text()"/></td>
		</tr>
	</xsl:template>


	<!-- add Rank -->
	<xsl:template mode="RecHonours" match="emph[@altrender='rank']">
			<tr class="medalRow">
				<td class="medalheader"> Rank: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>	


	<!-- add Regiment No -->
	<xsl:template mode="RecHonours" match="emph[@altrender='regno']">
			<tr class="medalRow">
				<td class="medalheader"> Service No: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>		
	

	<!-- add Corps -->
	<xsl:template mode="RecHonours" match="corpname">
			<tr class="medalRow">
				<td class="medalheader"> Regiment: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>	


	<!-- add Corps -->
	<xsl:template mode="RecHonours" match="geogname">
			<tr class="medalRow">
				<td class="medalheader"> Theatre of Combat or Operation: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>	


	<!-- add Regiment No -->
	<xsl:template mode="RecHonours" match="emph[@altrender='award']">
			<tr class="medalRow">
				<td class="medalheader"> Award: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>		

<!-- add Regiment No -->
	<xsl:template mode="RecHonours" match="emph[@altrender='date']">
			<tr class="medalRow">
				<td class="medalheader">  Date of announcement in London Gazette: </td>
				<td class="medalplain"><xsl:value-of select="text()" />
				</td></tr>
	</xsl:template>	


	<!-- add Folio -->
	<xsl:template mode="RecHonours" match="emph[@altrender='folio']">
			<tr class="medalRow">
				<td class="medalheader"> Folio: </td>
				<td class="medalplain"><xsl:value-of disable-output-escaping="yes"  select="text()" />
			</td></tr>
	</xsl:template>	
			
</xsl:stylesheet>
