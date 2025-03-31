<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html" />

  <xsl:include href="Will_DetailScope_inc.xsl" />
  <xsl:include href="Medal_DetailScope_inc.xsl" />
  <xsl:include href="SeamenMedal_DetailScope_inc.xsl" />
  <xsl:include href="Prisoner_DetailScope_inc.xsl" />
  <xsl:include href="DeathDuty_DetailScope_inc.xsl" />
  <xsl:include href="RegSea_DetailScope_inc.xsl" />
  <xsl:include href="MusterRolls_DetailScope_inc.xsl" />
  <xsl:include href="PrisonerInterview_DetailScope_inc.xsl" />
  <xsl:include href="RecHonours_DetailScope_inc.xsl" />
  <xsl:include href="VictoriaCross_DetailScope_inc.xsl" />
  <xsl:include href="WomensCorps_DetailScope_inc.xsl" />
  <xsl:include href="NavyLandService_DetailScope_inc.xsl" />
  <xsl:include href="AncientPetitions_DetailScope_inc.xsl" />
  <xsl:include href="AliensRegCards_DetailScope_inc.xsl" />
  <xsl:include href="Domesday_DetailScope_inc.xsl" />
  <xsl:include href="CombatReportsWW2_DetailScope_inc.xsl" />
  <xsl:include href="SeamenWill_DetailScope_inc.xsl" />
  <xsl:include href="Airwomen_DetailScope_inc.xsl" />
  <xsl:include href="Wrns_DetailScope_inc.xsl" />
  <xsl:include href="PoorLaw_DetailScope_inc.xsl" />
  <xsl:include href="CabinetPapers_DetailScope_inc.xsl" />
  <xsl:include href="RNOfficer_DetailScope_inc.xsl" />
  <xsl:include href="RNVRWW1_DetailScope_inc.xsl" />
  <xsl:include href="RoyalMarines_DetailScope_inc.xsl" />
  <xsl:include href="RegShipSea_DetailScope_inc.xsl" />
  <xsl:include href="RAFOfficers_DetailScope_inc.xsl" />
  <xsl:include href="BritishWarMedal_DetailScope_inc.xsl" />
  <xsl:include href="RoyalNavalReserve_DetailScope_inc.xsl" />
  <xsl:include href="MedievalSealRecords_DetailScope_inc.xsl" />
  <xsl:include href="NavalOfficers_DetailScope_inc.xsl" />
  <xsl:include href="LootedArt_DetailScope_inc.xsl" />
  <xsl:include href="NursingService_DetailScope_inc.xsl" />
  <xsl:include href="Titanic_DetailScope_inc.xsl" />
  <xsl:include href="Squadron_SimpleScope_inc.xsl" />
  <xsl:include href="Olympic_SimpleScope_inc.xsl" />
  <xsl:include href="RNASOfficers_DetailScope_inc.xsl" />
  <xsl:include href="HomeOfficeGeorgeIII_DetailScope_inc.xsl" />
  <xsl:include href="HomeOfficeDNPC_DetailScope_inc.xsl" />
  <xsl:include href="GallantrySea_DetailScope_inc.xsl" />
  <xsl:include href="EffectsPapers_DetailScope_inc.xsl" />
  <xsl:include href="Cavalry_DetailScope_inc.xsl" />
  <xsl:include href="NavalReserveOfficers_DetailScope_inc.xsl" />
  <xsl:include href="FameWill_DetailScope_inc.xsl" />
  <xsl:include href="StandardScope_inc.xsl" />

  <xsl:template match="/">
    <!--
		VERSION CONTROL	ImageDetailsDisplay XSL STYLESHEET

		###	VERSION: 1.0 	AUTHOR: RBEASLEY	DATE: 07/10/2003
		Created.

		###	VERSION: 1.1 	AUTHOR: RBEASLEY	DATE: 27/10/2003
		Updated.
			Renamed include files to '_inc' rather than '_XSL'

		###	VERSION: 1.2 	AUTHOR: CDICKSON	DATE: 08/07/2004
		Updated.
			Added logic for seamen medal
		-->
    <xsl:call-template name="colltype" />
  </xsl:template>

  <xsl:template name="colltype">
    <xsl:choose>

      <!-- Show the entire will text to display -->
      <xsl:when test="colltype/@id = 'Will'">
        <xsl:apply-templates mode="will" />
      </xsl:when>

      <!-- Process the entire medal text to display in html table -->
      <xsl:when test="colltype/@id = 'Medal'">
        <table>
          <xsl:apply-templates mode="medal" />
        </table>
      </xsl:when>

      <!-- Process the entire seamen medal text to display in html table -->
      <xsl:when test="colltype/@id = 'SeamenMedal'">
        <table>
          <xsl:apply-templates mode="seamenmedal" />
        </table>
      </xsl:when>

      <!-- Process the prisoner text to display in html table -->
      <xsl:when test="colltype/@id = 'prisoner'">
        <table>
          <xsl:apply-templates mode="prisoner" />
        </table>
      </xsl:when>

      <!-- Process the death duty text to display in html table -->
      <xsl:when test="colltype/@id = 'DeathDuty'">
        <xsl:apply-templates mode="deathduty" />
      </xsl:when>

      <!-- Process the SeamenRegister text to display in html table -->
      <xsl:when test="colltype/@id = 'SeamenRegister'">
        <table>
          <xsl:apply-templates mode="SeamenRegister" />
        </table>
      </xsl:when>

      <!-- Process the MusterRolls text to display in html table -->
      <xsl:when test="colltype/@id = 'MusterRolls'">
        <table>
          <xsl:apply-templates mode="MusterRolls" />
        </table>
      </xsl:when>

      <!-- Process the PrisonerInterview text to display in html table -->
      <xsl:when test="colltype/@id = 'PrisonerInterview'">
        <table>
          <xsl:apply-templates mode="PrisonerInterview" />
        </table>
      </xsl:when>

      <!-- Process the RecHonours text to display in html table -->
      <xsl:when test="colltype/@id = 'RecHonours'">
        <table>
          <xsl:apply-templates mode="RecHonours" />
        </table>
      </xsl:when>

      <!-- Process the VictoriaCross text to display in html table -->
      <xsl:when test="colltype/@id = 'VictoriaCross'">
        <table>
          <xsl:apply-templates mode="VictoriaCross" />
        </table>
      </xsl:when>

      <!-- Process the WomensCorps text to display in html table -->
      <xsl:when test="colltype/@id = 'WomensCorps'">
        <table>
          <xsl:apply-templates mode="WomensCorps" />
        </table>
      </xsl:when>

      <!-- Process the NavyLandService text to display in html table -->
      <xsl:when test="colltype/@id = 'NavyLandService'">
        <table>
          <xsl:apply-templates mode="NavyLandService" />
        </table>
      </xsl:when>

      <!-- Process the NavyLandService text to display in html table -->
      <xsl:when test="colltype/@id = 'AncientPetitions'">
        <table>
          <xsl:apply-templates mode="AncientPetitions" />
        </table>
      </xsl:when>

      <!-- Process the AlienRegistrationCards text to display in html table -->
      <xsl:when test="colltype/@id = 'AliensRegCards'">
        <table>
          <xsl:apply-templates mode="AliensRegCards" />
        </table>
      </xsl:when>

      <!-- Process the AlienRegistrationCards text to display in html table -->
      <xsl:when test="colltype/@id = 'DomesdayBook'">
        <table>
          <xsl:apply-templates mode="DomesdayBook" />
        </table>
      </xsl:when>

      <!-- Process the Combat Reports WW2 text to display in html table -->
      <xsl:when test="colltype/@id = 'CombatRepWW2'">
        <table>
          <xsl:apply-templates mode="CombatRepWW2" />
        </table>
      </xsl:when>

      <!-- Process the Combat Reports WW2 text to display in html table -->
      <xsl:when test="colltype/@id = 'Airwomen'">
        <table>
          <xsl:apply-templates mode="Airwomen" />
        </table>
      </xsl:when>

      <!-- Process the Seamen Will text to display in html table -->
      <xsl:when test="colltype/@id = 'SeamenWill'">
        <table>
          <xsl:apply-templates mode="SeamenWill" />
        </table>
      </xsl:when>

      <!-- Process the Seamen Will text to display in html table -->
      <xsl:when test="colltype/@id = 'Wrns'">
        <table>
          <xsl:apply-templates mode="Wrns" />
        </table>
      </xsl:when>

      <!-- Process the PoorLaw text to display in html table -->
      <xsl:when test="colltype/@id = 'PoorLaw'">
        <table>
          <xsl:apply-templates mode="PoorLaw" />
        </table>
      </xsl:when>

      <!-- Process the CabinetPapers text to display in html table -->
      <xsl:when test="colltype/@id = 'CabinetPapers'">
        <table>
          <xsl:apply-templates mode="CabinetPapers" />
        </table>
      </xsl:when>

      <!-- Process the RNOfficer text to display in html table -->
      <xsl:when test="colltype/@id = 'RNOfficer'">
        <table>
          <xsl:apply-templates mode="RNOfficer" />
        </table>
      </xsl:when>

      <!-- Process the RNVRWW1 text to display in html table -->
      <xsl:when test="colltype/@id = 'VolunteerReserve'">
        <table>
          <xsl:apply-templates mode="VolunteerReserve" />
        </table>
      </xsl:when>

      <!-- Process the RNVRWW1 text to display in html table -->
      <xsl:when test="colltype/@id = 'RoyalMarines'">
        <table>
          <xsl:apply-templates mode="RoyalMarines" />
        </table>
      </xsl:when>

      <!-- Process the RegShipSea text to display in html table -->
      <xsl:when test="colltype/@id = 'ShippingSeamen'">
        <table>
          <xsl:apply-templates mode="ShippingSeamen" />
        </table>
      </xsl:when>

      <!-- Process the RAFOfficers text to display in html table -->
      <xsl:when test="colltype/@id = 'RAFOfficers'">
        <table>
          <xsl:apply-templates mode="RAFOfficers" />
        </table>
      </xsl:when>

      <!-- Process the BritishWarMedal text to display in html table -->
      <xsl:when test="colltype/@id = 'BritishWarMedal'">
        <table>
          <xsl:apply-templates mode="BritishWarMedal" />
        </table>
      </xsl:when>

      <!-- Process the Royal Naval Reserve text to display in html table -->
      <xsl:when test="colltype/@id = 'NavalReserve'">
        <table>
          <xsl:apply-templates mode="NavalReserve" />
        </table>
      </xsl:when>

      <!-- Process the Royal Naval Reserve text to display in html table -->
      <xsl:when test="colltype/@id = 'MedSeal'">
        <table>
          <xsl:apply-templates mode="MedSeal" />
        </table>
      </xsl:when>

      <!-- Process the Royal Naval Reserve text to display in html table -->
      <xsl:when test="colltype/@id = 'NavalOfficers'">
        <table>
          <xsl:apply-templates mode="NavalOfficers" />
        </table>
      </xsl:when>

      <!-- Process the Looted Art text to display in html table -->
      <xsl:when test="colltype/@id = 'LootedArt'">
        <table>
          <xsl:apply-templates mode="LootedArt" />
        </table>
      </xsl:when>

      <!-- Process the Nursing Service Records text to display in html table -->
      <xsl:when test="colltype/@id = 'NursingService'">
        <table>
          <xsl:apply-templates mode="NursingService" />
        </table>
      </xsl:when>

      <!-- Process the Nursing Service Records text to display in html table -->
      <xsl:when test="colltype/@id = 'Titanic'">
        <table>
          <xsl:apply-templates mode="Titanic" />
        </table>
      </xsl:when>

      <!-- Process the Squadron Operations Records text to display in html table -->
      <xsl:when test="colltype/@id = 'Squadron'">
        <table>
          <xsl:apply-templates mode="Squadron" />
        </table>
      </xsl:when>

      <!-- Process the Olympic Records text to display in html table -->
      <xsl:when test="colltype/@id = 'Olympic'">
        <table>
          <xsl:apply-templates mode="Olympic" />
        </table>
      </xsl:when>

      <!-- Process the  RNAS Officer's Services text to display in html table -->
      <xsl:when test="colltype/@id = 'RNASOfficers'">
        <!--<table>-->
        <xsl:apply-templates mode="RNASOfficers" />
        <!--</table>-->
      </xsl:when>

      <!-- Process the  Home Office George III records text to display in html table -->
      <xsl:when test="colltype/@id = 'HomeOfficeGeorge'">
        <table>
          <xsl:apply-templates mode="HomeOfficeGeorge" />
        </table>
      </xsl:when>

      <!-- Process the Home Office: Denization and Naturalisation papers records text to display in html table -->
      <xsl:when test="colltype/@id = 'DNPC'">
        <table>
          <xsl:apply-templates mode="DNPC" />
        </table>
      </xsl:when>

      <!-- Process the Marine Divisions: Gallantry at Sea Awards records text to display in html table -->
      <xsl:when test="colltype/@id = 'GallantrySea'">
        <table>
          <xsl:apply-templates mode="GallantrySea" />
        </table>
      </xsl:when>

      <!-- Process the Admiralty, Officers' and Civilians' Effects Papers records text to display in html table -->
      <xsl:when test="colltype/@id = 'EffectsPapers'">
        <table>
          <xsl:apply-templates mode="EffectsPapers" />
        </table>
      </xsl:when>

      <!-- Process the Soldiers' Documents: The Household Cavalry records text to display in html table -->
      <xsl:when test="colltype/@id = 'Cavalry'">
        <table>
          <xsl:apply-templates mode="Cavalry" />
        </table>
      </xsl:when>

      <!-- Process the Royal Naval Reserve Officers' Service Records text to display in html table -->
      <xsl:when test="colltype/@id = 'NavalReserveOfficers'">
        <table>
          <xsl:apply-templates mode="NavalReserveOfficers" />
        </table>
      </xsl:when>

      <!-- Process the Famous Wills text to display in html table -->
      <xsl:when test="(colltype/@id = 'FameWill') or (colltype/@id = 'Miscellaneous') or (colltype/@id = 'Miscellaneous')
                or (colltype/@id = 'Opening2002') or (colltype/@id = 'MapPicture') or (colltype/@id = 'Opening2003')
                or (colltype/@id = 'APS')">
        <xsl:apply-templates mode="FameWill" />
      </xsl:when>

      <!-- Display standard text -->
      <xsl:otherwise>
        <xsl:apply-templates mode="standard" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>