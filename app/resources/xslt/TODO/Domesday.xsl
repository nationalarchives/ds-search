<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		###	VERSION: 1.1 	AUTHOR: MHILLYARD	DATE: 23/03/2006
		Modified.
		-->
	</xsl:template>


	<!-- ignore 'doctype' text (should be 'D') -->
	<xsl:template mode="DomesdayBook" match="emph[@altrender='doctype']">
	</xsl:template>


	<!-- add Corps -->
	<xsl:template mode="DomesdayBook" match="geogname">
			<tr class="medalRow">
				<td class="medalheader"> Place name: </td>
				<td class="medalplain"><xsl:value-of disable-output-escaping="yes"  select="text()" />
				</td></tr>
	</xsl:template>	

	<!-- add Places mentioned -->
	<xsl:template mode="DomesdayBook" match="emph[@altrender='domesdayform']">
	 <tr class="medalRow">
	  <td class="medalheader"> Domesday place name: </td>
	  <td class="medalplain">
	   <xsl:for-each select="./geogname">
	     <xsl:value-of select="text()" />
	     <xsl:if test="following-sibling::geogname">
	      <xsl:text disable-output-escaping="yes">; </xsl:text>
	     </xsl:if>
	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>	

	<!-- add Folio -->
	<xsl:template mode="DomesdayBook" match="emph[@altrender='folio']">
			<tr class="medalRow">
				<td class="medalheader"> Folio: </td>
				<td class="medalplain"><xsl:value-of disable-output-escaping="yes"  select="text()" />
				</td></tr>
	</xsl:template>	


	<!-- add Places mentioned -->
	<xsl:template mode="DomesdayBook" match="emph[@altrender='placesmentioned']">
	 <tr class="medalRow">
	  <td class="medalheader"> Places mentioned: </td>
	  <td class="medalplain">
	   <xsl:for-each select="./geogname">
	     <xsl:value-of select="text()" />
	     <xsl:if test="following-sibling::geogname">
	      <xsl:text disable-output-escaping="yes">; </xsl:text>
	     </xsl:if>
	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>	


	<!-- add Places mentioned -->
	<xsl:template mode="DomesdayBook" match="emph[@altrender='peoplementioned']">
	 <tr class="medalRow">
	  <td class="medalheader"> People mentioned within entire folio: </td>
	  <td class="medalplain">
	   <xsl:for-each select="./persname">
	     <xsl:value-of select="text()" />
	     <xsl:if test="following-sibling::persname">
	      <xsl:text disable-output-escaping="yes">; </xsl:text>
	     </xsl:if>
	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>	

</xsl:stylesheet>
