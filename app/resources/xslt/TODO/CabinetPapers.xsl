<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	CabinetPapers_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		###	VERSION: 1.1 	AUTHOR: MHILLYARD	DATE: 23/03/2006
		Modified.
		###	VERSION: 1.2 	AUTHOR: MHILLYARD	DATE: 25/04/2007
		Modified.
		-->
	</xsl:template>


	<!-- ignore 'doctype' text (should be 'CP') -->
	<xsl:template mode="CabinetPapers" match="emph[@altrender='doctype']">
	</xsl:template>


	<!-- add surname mentioned -->
	<xsl:template mode="CabinetPapers" match="emph[@altrender='surname']">
	 <tr class="medalRow">
	  <td class="medalplain"> Attendees: </td>
	  <td class="medalplain">
	   <xsl:for-each select="./surname">
	     <xsl:value-of disable-output-escaping="yes" select="text()" />
	     <xsl:if test="following-sibling::surname">
	      <xsl:text disable-output-escaping="yes">; </xsl:text>
	     </xsl:if>
	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>	

	<!-- add Date  -->
	<xsl:template mode="CabinetPapers" match="emph[@altrender='agenda']">
			<tr class="medalRow">
			<td class="medalplain">  Agenda: </td>
			<td class="medalplain"><xsl:value-of select="text()" />
		</td></tr>
	</xsl:template>	

	<!-- add Former Reference  -->
	<xsl:template mode="CabinetPapers" match="emph[@altrender='formerreference']">
			<tr class="medalRow">
			<td class="medalplain">  Former Reference: </td>
			<td class="medalplain"><xsl:value-of select="text()" />
		</td></tr>
	</xsl:template>	

	<!-- add Record Type  -->
	<xsl:template mode="CabinetPapers" match="emph[@altrender='type']">
			<tr class="medalRow">
			<td class="medalplain">  Record Type: </td>
			<td class="medalplain"><xsl:value-of select="text()" />
		</td></tr>
	</xsl:template>	
	
	
	<!-- add Title  -->
	<xsl:template mode="CabinetPapers" match="emph[@altrender='title']">
			<tr class="medalRow">
			<td class="medalplain">  Title: </td>
			<td class="medalplain"><xsl:value-of select="text()" />
			</td></tr>
	</xsl:template>	

	<!-- add Author  -->
	<xsl:template mode="CabinetPapers" match="emph[@altrender='author']">
			<tr class="medalRow">
			<td class="medalplain">  Author: </td>
			<td class="medalplain"><xsl:value-of select="text()" />
		</td></tr>
	</xsl:template>	
	
</xsl:stylesheet>

