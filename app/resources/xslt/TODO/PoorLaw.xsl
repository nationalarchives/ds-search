<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html"/>

	<xsl:template match="version">
		<!--
		VERSION CONTROL	SeamenMedal_SimpleScope_XSL XSL STYLESHEET
	
		###	VERSION: 1.0 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Created.
		###	VERSION: 1.1 	AUTHOR: MHILLYARD	DATE: 23/03/2006
		Modified.
		###	VERSION: 1.2 	AUTHOR: MHILLYARD	DATE: 25/04/2007
		Modified.
		-->
	</xsl:template>


	<!-- ignore 'doctype' text (should be 'PL') -->
	<xsl:template mode="PoorLaw" match="emph[@altrender='doctype']">
	</xsl:template>


	<!-- Display lastname, firstname -->
	<xsl:template mode="PoorLaw" match="persname">
	<tr class="medalRow">
	 <td class="medalheader" width="20%"><xsl:text disable-output-escaping="yes">Name(s): </xsl:text></td>
	 <td class="medalplain" width="50%">
  
		<xsl:if test="emph[@altrender='surname'] and emph[@altrender='forenames']">

		<xsl:variable name="NumberOfPeople">
		 <xsl:value-of select="count(./emph[@altrender='surname']/surname)" />
		</xsl:variable>
		
		<xsl:for-each select="./emph[@altrender='surname']/surname">
		
		 <xsl:variable name="NamePos">
		  <xsl:value-of select="position()" />
		 </xsl:variable>
		
		 <xsl:if test="not(position() &gt; $NumberOfPeople)">
		  <xsl:value-of select="."/>
		  <xsl:text>, </xsl:text>
		
		  <xsl:for-each select="../../emph[@altrender='forenames']/firstname">
		   <xsl:if test="(position() = $NamePos)">
		    <xsl:value-of select="."/>
		    <xsl:if test="not(position() = last())">
		     <xsl:text>; </xsl:text>
		    </xsl:if>
		   </xsl:if>
		  </xsl:for-each>
		
		 </xsl:if>
		</xsl:for-each>

		</xsl:if>

	 </td>
	</tr>
	</xsl:template>


	<!-- add Places mentioned -->
	<xsl:template mode="PoorLaw" match="emph[@altrender='placesmentioned']">
	 <tr class="medalRow">
	  <td class="medalheader"> Places mentioned: </td>
	  <td class="medalplain">
	   <xsl:for-each select="./geogname">
	     <xsl:value-of disable-output-escaping="yes" select="text()" />
	     <xsl:if test="following-sibling::geogname">
	      <xsl:text disable-output-escaping="yes">; </xsl:text>
	     </xsl:if>
	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>		


	<!-- add Places mentioned -->
	<xsl:template mode="PoorLaw" match="emph[@altrender='orgsmentioned']">
	 <tr class="medalRow">
	  <td class="medalheader"> Corporations: </td>
	  <td class="medalplain">
	   <xsl:for-each select="./corpname">
	     <xsl:value-of disable-output-escaping="yes" select="text()" />
	     <xsl:if test="following-sibling::corpname">
	      <xsl:text disable-output-escaping="yes">; </xsl:text>
	     </xsl:if>
	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>	


	<!-- add Places mentioned -->
	<xsl:template mode="PoorLaw" match="emph[@altrender='occupation']">
	 <tr class="medalRow">
	  <td class="medalheader"> Occupation: </td>
	  <td class="medalplain">
	   <xsl:for-each select="./occupation">
	     <xsl:value-of disable-output-escaping="yes" select="text()" />
	     <xsl:if test="following-sibling::occupation">
	      <xsl:text disable-output-escaping="yes">; </xsl:text>
	     </xsl:if>
	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>	
	
	
	<!-- add Date  -->
	<xsl:template mode="PoorLaw" match="emph[@altrender='date']">
			<tr class="medalRow">
			<td class="medalplain">  Date of correspondence: </td>
			<td class="medalplain"><xsl:value-of disable-output-escaping="yes" select="text()" />
		</td></tr>
	</xsl:template>	

	<!-- add scope -->
	<xsl:template mode="PoorLaw" match="emph[@altrender='scope']">
	 <xsl:variable name="scope">
	  <xsl:for-each select="p | ul/li">
	   <xsl:value-of select="."/>
	  </xsl:for-each>
	 </xsl:variable>

	 <tr class="medalRow">
	  <td class="medalplain"> Content: </td>
	  <td class="medalplain">

	   <xsl:for-each select="p | ul">
	    <!--xsl:copy-of select="."/-->
	    <table>
	     <xsl:for-each select="descendant-or-self::*">
	      <xsl:choose>

	       <xsl:when test="self::ul">
	        <tr><td><ul>
	         <xsl:for-each select="child::li">
	          <li />
	          <xsl:value-of disable-output-escaping="yes" select="."/>
	         </xsl:for-each>
	        </ul></td></tr>
	       </xsl:when>

	       <xsl:when test="self::p">
	        <tr><td>
	         <xsl:value-of disable-output-escaping="yes" select="."/>
	        </td></tr>
	       </xsl:when>
	      </xsl:choose>
	     </xsl:for-each>
	    </table>

	   </xsl:for-each>
	  </td>
	 </tr>
	</xsl:template>			

	
	<!-- add Scope2 -->
	<xsl:template mode="PoorLaw" match="emph[@altrender='scope2']">
	<tr class="medalRow">
	<td class="medalheader" width="30%"><xsl:text disable-output-escaping="yes">Content: </xsl:text> </td>
	<td class="medalplain" width="60%"><xsl:value-of disable-output-escaping="yes" select="text()" />
	</td></tr>
	</xsl:template>



</xsl:stylesheet>

