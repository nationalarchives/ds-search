<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	Will_DetailScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: RBEASLEY	DATE: 10/10/2003
		Created.
		-->
	</xsl:template>
	
	<!-- ignore 'doctype' text (should be 'AR') -->
		<xsl:template mode="AliensRegCards" match="emph[@altrender='doctype']">
		</xsl:template>
		
		
			
			<!-- show title and " "-->
			<xsl:template mode="AliensRegCards" match="emph[@altrender='perstitle']">
				<tr class="medalRow">
					<td class="medalplain">Title: </td>
					<td class="medalplain"><xsl:value-of select="text()" />
					</td></tr>
			</xsl:template>
			
			
			
			<!-- Display lastname, firstname -->
				<xsl:template mode="AliensRegCards" match="persname">
					<tr class="medalRow">
						<td class="medalplain" width="25%"><xsl:text disable-output-escaping="yes">Name: </xsl:text></td>
						<td class="medalplain" width="60%"><xsl:value-of select="emph[@altrender='forenames']/text()"/>
						<xsl:if test="emph[@altrender='forenames'] and emph[@altrender='surname']">
							<xsl:text disable-output-escaping="yes"> </xsl:text>
						</xsl:if>
						<xsl:value-of select="emph[@altrender='surname']/text()"/></td>
					</tr>
			</xsl:template>
			
	
			<!-- add DOB -->
			<xsl:template mode="AliensRegCards" match="emph[@altrender='age']">
				<tr class="medalRow">
					<td class="medalplain">Date of Birth: </td>
					<td class="medalplain"><xsl:value-of select="text()" />
					</td></tr>
			</xsl:template>	
	
	
	
			<!-- add Nationality -->
			<xsl:template mode="AliensRegCards" match="emph[@altrender='nation']">
				<tr class="medalRow">
					<td class="medalplain">Nationality: </td>
					<td class="medalplain"><xsl:value-of select="text()" />
					</td></tr>
		</xsl:template>

  <!-- add Date of Birth -->
  <xsl:template mode="AliensRegCards" match="emph[@altrender='dob']">
    <tr class="medalRow">
      <td class="medalheader"> Date of Birth: </td>
      <td class="medalplain">
        <xsl:value-of select="text()" />
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
