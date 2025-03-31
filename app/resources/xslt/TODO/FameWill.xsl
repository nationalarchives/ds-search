<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:output method="html" />

  <xsl:template match="version">
    <!--
		VERSION CONTROL	FameWill_DetailScope_XSL XSL STYLESHEET

		###	VERSION: 1.0 	AUTHOR: RDICKINSON	DATE: 07/08/2013
		Created.
		-->
  </xsl:template>

  <!-- write 'doctype' static text depending on value -->
  <!--
	<xsl:template mode="FameWill" match="emph[@altrender='doctype']">
	-->
  <!--tr class="medalRow"-->
  <!--
	<td class="medalplain" width="20%">
		<xsl:choose>
			<xsl:when test="text() = 'W'">
				<xsl:text>Will of </xsl:text>
			</xsl:when>
			<xsl:when test="text() = 'P'">
				<xsl:text>Papers relating to </xsl:text>
			</xsl:when>
		</xsl:choose>
	</td>

	-->
  <!--td class="medalplain">
		<xsl:value-of select="emph[@altrender='surname']/text()" />
			<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">
		<xsl:text disable-output-escaping="yes">, </xsl:text>
		</xsl:if>
		<xsl:value-of select="emph[@altrender='forenames']/text()" />
	</td-->
  <!--/tr-->
  <!--
	</xsl:template>-->

  
  <xsl:template mode="FameWill" match="emph[@altrender='doctype']">
  </xsl:template>

  <!-- show title and " "-->
  <xsl:template mode="FameWill" match="emph[@altrender='perstitle']">
    <xsl:value-of select="text()" />
    <xsl:text> </xsl:text>
  </xsl:template>

  <!-- show firstname " " lastname -->
  <xsl:template mode="FameWill" match="persname">
    <xsl:value-of select="emph[@altrender='forenames']/text()" />
    <xsl:if test="emph[@altrender='surname']">
      <xsl:text disable-output-escaping="yes"> </xsl:text>
      <xsl:value-of select="emph[@altrender='surname']/text()" />
    </xsl:if>
    <xsl:text> </xsl:text>
  </xsl:template>
  
    <!--Replace NEWLINE chars with <br/>-->
  <xsl:template mode="FameWill" match="text()">
     <xsl:call-template name="replace">
          <xsl:with-param name="string" select="." />
        </xsl:call-template>
  </xsl:template>  
    
  <xsl:template name="replace">
    <xsl:param name="string" />
    <xsl:choose>
      <xsl:when test="contains($string,'&#10;')">
        <xsl:value-of select="substring-before($string,'&#10;')" />
        <br />
        <xsl:call-template name="replace">
          <xsl:with-param name="string" select="substring-after($string,'&#10;')" />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$string" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>