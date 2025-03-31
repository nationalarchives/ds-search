<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
	</xsl:template>

	<!-- ignore 'doctype' text (should be 'SQ') -->
	<xsl:template mode="Squadron" match="emph[@altrender='doctype']">
	</xsl:template>

	<!-- add Squadron Number -->
	<xsl:template mode="Squadron" match="emph[@altrender='num']">
	<tr class="medalRow">
		<td class="medalplain" width="30%"><xsl:text disable-output-escaping="yes">  Squadron Number:  </xsl:text> </td>
		<td class="medalplain" width="60%"><xsl:value-of disable-output-escaping="yes" select="text()" />
	</td></tr>
	</xsl:template>	

	<!-- add Summary of Events -->
	<xsl:template mode="Squadron" match="emph[@altrender='sum']">
	<tr class="medalRow">
		<td class="medalplain" width="30%"><xsl:text disable-output-escaping="yes">  Summary of Events:  </xsl:text> </td>
		<td class="medalplain" width="60%"><xsl:value-of disable-output-escaping="yes" select="text()" />
	</td></tr>
	</xsl:template>	
	
	<!-- add Records of Events -->
	<xsl:template mode="Squadron" match="emph[@altrender='rec']">
	<tr class="medalRow">
		<td class="medalplain" width="30%"><xsl:text disable-output-escaping="yes">  Records of Events:  </xsl:text> </td>
		<td class="medalplain" width="60%"><xsl:value-of disable-output-escaping="yes" select="text()" />
	</td></tr>
	</xsl:template>		
	
	<!-- add Appendices -->
	<xsl:template mode="Squadron" match="emph[@altrender='append']">
	<tr class="medalRow">
		<td class="medalplain" width="30%"><xsl:text disable-output-escaping="yes">  Appendices:  </xsl:text> </td>
		<td class="medalplain" width="60%"><xsl:value-of disable-output-escaping="yes" select="text()" />
	</td></tr>
	</xsl:template>

  <!-- add Comments -->
  <xsl:template mode="Squadron" match="emph[@altrender='comments']">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes">  Comments:  </xsl:text></td>
      <td class="medalplain" width="60%"><xsl:value-of disable-output-escaping="yes" select="text()" />
      </td>
    </tr>
  </xsl:template>
	
</xsl:stylesheet>

