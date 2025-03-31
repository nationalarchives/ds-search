<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
	</xsl:template>

	<!-- ignore 'doctype' text (should be 'RR') -->
	<xsl:template mode="NavalReserve" match="emph[@altrender='doctype']">
	</xsl:template>


	<!-- Display lastname, firstname -->
	<xsl:template mode="NavalReserve" match="persname">
		<tr class="medalRow">
		<td class="medalplain" width="30%"><xsl:text disable-output-escaping="yes">Name </xsl:text></td>
		<td class="medalplain" width="60%"><xsl:value-of select="emph[@altrender='surname']/text()"/>
		<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
			<xsl:text disable-output-escaping="yes">, </xsl:text>
		</xsl:if>

		<xsl:value-of select="emph[@altrender='perstitle']/text()"/>

		<xsl:if test="emph[@altrender='perstitle']">
			<xsl:text disable-output-escaping="yes"> </xsl:text>

		</xsl:if>
		<xsl:value-of select="emph[@altrender='forenames']/text()"/></td>
		</tr>
	</xsl:template>

	
	<!-- add Place of Birth -->
	<xsl:template mode="NavalReserve" match="geogname">
			<tr class="medalRow">
			<td class="medalheader"> Place of Birth: </td>
			<td class="medalplain"><xsl:value-of select="text()" />
		</td></tr>
	</xsl:template>		

	<!-- add Remarks -->
	<xsl:template mode="NavalReserve" match="emph[@altrender='certno']">
			<tr class="medalRow">
			<td class="medalplain">  Number:  </td>
			<td class="medalplain"><xsl:value-of select="text()" />
		</td></tr>
	</xsl:template>

  <!-- add Date of Birth -->
  <xsl:template mode="NavalReserve" match="emph[@altrender='dob']">
    <tr class="medalRow">
      <td class="medalheader"> Date of Birth: </td>
      <td class="medalplain"><xsl:value-of select="text()" />
      </td>
    </tr>
  </xsl:template>

</xsl:stylesheet>

