<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>
  <xsl:template match="version">
    <!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		-->
  </xsl:template>
  <!-- ignore 'doctype' text (should be 'MSR') -->
  <xsl:template match="emph[@altrender='doctype']">
	</xsl:template>
  <!-- add people mentioned -->
  <xsl:template match="persname">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes"> Name : </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of disable-output-escaping="yes" select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Places mentioned -->
  <xsl:template match="geogname">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes"> Places : </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of disable-output-escaping="yes" select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Document Note -->
  <xsl:template match="emph[@altrender='docnote']">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes">  Document Note:  </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of disable-output-escaping="yes" select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Seal Design -->
  <xsl:template match="emph[@altrender='sealdesign']">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes">  Seal Design:  </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of disable-output-escaping="yes" select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Material -->
  <xsl:template match="emph[@altrender='material']">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes">  Material:  </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of disable-output-escaping="yes" select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add Attachment -->
  <xsl:template match="emph[@altrender='attachment']">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes">  Attachment:  </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of disable-output-escaping="yes" select="text()"/>
      </td>
    </tr>
  </xsl:template>
  <!-- add sealnote -->
  <xsl:template match="emph[@altrender='sealnote']">
    <tr class="medalRow">
      <td class="medalplain" width="30%">
        <xsl:text disable-output-escaping="yes">  Seal Note:  </xsl:text>
      </td>
      <td class="medalplain" width="60%">
        <xsl:value-of disable-output-escaping="yes" select="text()"/>
      </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
