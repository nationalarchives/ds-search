<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	Cavalry_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'CV') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <!-- Display lastname, firstname -->
  <xsl:template match="persname">
    <tr class="medalRow">
      <td class="medalplain" width="20%">
        <xsl:text>Name</xsl:text>
      </td>
      <td class="medalplain" width="50%">
        <xsl:value-of select="emph[@altrender='surname']/text()"/>
        <xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
          <xsl:text>, </xsl:text>
        </xsl:if>
        <xsl:value-of select="emph[@altrender='forenames']/text()"/>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
