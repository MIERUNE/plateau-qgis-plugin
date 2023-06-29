"""区域モデル (./area/)、都市計画決定情報モデル (./urf/)"""

# TODO: 都市計画決定情報の大分類にもとづいてレイヤを分けるのがよいか?
# 現状は、都市計画決定情報の全地物を1つのレイヤにまとめている

from .base import (
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
)


def _make_prefix_variants(prefixed_names: list[str]) -> list[str]:
    names = []
    for name in prefixed_names:
        assert name.startswith("urf:")
        n = name.split(":")[1]
        names.append("urf2:" + n)
        names.append("urf3:" + n)
    return names


URF_ZONE = FeatureProcessingDefinition(
    id="urf:Zone",
    target_elements=_make_prefix_variants(
        [
            "urf:AircraftNoiseControlZone",
            "urf:AreaClassification",
            "urf:CollectiveFacilitiesForReconstruction",
            "urf:CollectiveFacilitiesForReconstructionAndRevitalization",
            "urf:CollectiveFacilitiesForTsunamiDisasterPrevention",
            "urf:CollectiveGovernmentAndPublicOfficeFacilities",
            "urf:CollectiveHousingFacilities",
            "urf:CollectiveUrbanDisasterPreventionFacilities",
            "urf:ConservationZoneForClustersOfTraditionalStructures",
            "urf:DisasterPreventionBlockImprovementProject",
            "urf:DisasterPreventionBlockImprovementZonePlan",
            "urf:DistributionBusinessPark",
            "urf:DistributionBusinessZone",
            "urf:DistrictDevelopmentPlan",
            "urf:DistrictFacility",
            "urf:DistrictImprovementPlanForDisasterPreventionBlockImprovementZonePlan",
            "urf:DistrictImprovementPlanForHistoricSceneryMaintenanceAndImprovementDistrict",
            "urf:DistrictPlan",
            "urf:DistrictsAndZones",
            "urf:EducationalAndCulturalFacility",
            "urf:ExceptionalFloorAreaRateDistrict",
            "urf:FirePreventionDistrict",
            "urf:FireProtectionFacility",
            "urf:FloodPreventionFacility",
            "urf:GlobalHubCityDevelopmentProject",
            "urf:GreenSpaceConservationDistrict",
            "urf:HeightControlDistrict",
            "urf:HighLevelUseDistrict",
            "urf:HighRiseResidentialAttractionDistrict",
            "urf:HistoricSceneryMaintenanceAndImprovementDistrictPlan",
            "urf:HousingControlArea",
            "urf:IndustrialParkDevelopmentProject",
            "urf:LandReadjustmentProject",
            "urf:LandReadjustmentPromotionArea",
            "urf:LandReadjustmentPromotionAreasForCoreBusinessUrbanDevelopment",
            "urf:LandscapeZone",
            "urf:MarketsSlaughterhousesCrematoria",
            "urf:MedicalFacility",
            "urf:NewHousingAndUrbanDevelopmentProject",
            "urf:NewUrbanInfrastructureProject",
            "urf:OpenSpaceForPublicUse",
            "urf:ParkingPlaceDevelopmentZone",
            "urf:PortZone",
            "urf:PrivateUrbanRenewalProjectPlan",
            "urf:ProductiveGreenZone",
            "urf:ProjectPromotionArea",
            "urf:PromotionDistrict",
            "urf:QuasiUrbanPlanningArea",
            "urf:ResidenceAttractionArea",
            "urf:ResidentialBlockConstructionProject",
            "urf:ResidentialBlockConstructionPromotionArea",
            "urf:ResidentialEnvironmentImprovementDistrict",
            "urf:RoadsideDistrictFacility",
            "urf:RoadsideDistrictImprovementPlan",
            "urf:RoadsideDistrictPlan",
            "urf:RuralDistrictFacility",
            "urf:RuralDistrictImprovementPlan",
            "urf:RuralDistrictPlan",
            "urf:SandControlFacility",
            "urf:ScenicDistrict",
            "urf:ScheduledAreaForCollectiveGovernmentAndPublicOfficeFacilities",
            "urf:ScheduledAreaForCollectiveHousingFacilities",
            "urf:ScheduledAreaForDistributionBusinessPark",
            "urf:ScheduledAreaForIndustrialParkDevelopmentProjects",
            "urf:ScheduledAreaForNewHousingAndUrbanDevelopmentProjects",
            "urf:ScheduledAreaForNewUrbanInfrastructureProjects",
            "urf:ScheduledAreaForUrbanDevelopmentProject",
            "urf:SnowProtectionFacility",
            "urf:SocialWelfareFacility",
            "urf:SpecialGreenSpaceConservationDistrict",
            "urf:SpecialUrbanRenaissanceDistrict",
            "urf:SpecialUseAttractionDistrict",
            "urf:SpecialUseDistrict",
            "urf:SpecialUseRestrictionDistrict",
            "urf:SpecialZoneForPreservationOfHistoricalLandscape",
            "urf:SpecifiedBlock",
            "urf:SpecifiedBuildingZoneImprovementPlan",
            "urf:SpecifiedDisasterPreventionBlockImprovementZone",
            "urf:SpecifiedUrgentUrbanRenewalArea",
            "urf:SupplyFacility",
            "urf:TelecommunicationFacility",
            "urf:TideFacility",
            "urf:TrafficFacility",
            "urf:TreatmentFacility",
            "urf:TreePlantingDistrict",
            "urf:UnclassifiedBlankArea",
            "urf:UnclassifiedUseDistrict",
            "urf:UnusedLandUsePromotionArea",
            "urf:UrbanDevelopmentProject",
            "urf:UrbanDisasterRecoveryPromotionArea",
            "urf:UrbanFacility",
            "urf:UrbanFacilityStipulatedByCabinetOrder",
            "urf:UrbanFunctionAttractionArea",
            "urf:UrbanPlanningArea",
            "urf:UrbanRedevelopmentProject",
            "urf:UrbanRedevelopmentPromotionArea",
            "urf:UrbanRenewalProject",
            "urf:UrgentUrbanRenewalArea",
            "urf:UseDistrict",
            "urf:Waterway",
            "urf:WindProtectionFacility",
            "urf:ZonalDisasterPreventionFacility",
            "urf:ZoneForPreservationOfHistoricalLandscape",
        ]
    ),
    lod_detection=LODDetection(
        lod1=["./urf:lod1MultiSurface"],
    ),
    attribute_groups=[
        # attributes inherited from urf:Zone
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="function",
                    path="./urf:function",
                    datatype="[]string",
                    predefined_codelist=None,
                ),
                Attribute(
                    name="usage",
                    path="./urf:usage",
                    datatype="[]string",
                    predefined_codelist=None,
                ),
                Attribute(
                    name="validFrom",
                    path="./urf:validFrom",
                    datatype="date",
                ),
                Attribute(
                    name="validFromType",
                    path="./urf:validFromType",
                    datatype="string",
                    predefined_codelist="Common_validType",
                ),
                Attribute(
                    name="validTo",
                    path="./urf:validTo",
                    datatype="date",
                ),
                Attribute(
                    name="validToType",
                    path="./urf:validToType",
                    datatype="string",
                    predefined_codelist="Common_validType",
                ),
                Attribute(
                    name="expirationFiscalYear",
                    path="./urf:expirationFiscalYear",
                    datatype="integer",
                ),
                Attribute(
                    name="legalGrounds",
                    path="./urf:legalGrounds",
                    datatype="string",
                ),
                Attribute(
                    name="custodian",
                    path="./urf:custodian",
                    datatype="string",
                ),
                Attribute(
                    name="notificationNumber",
                    path="./urf:notificationNumber",
                    datatype="string",
                ),
                Attribute(
                    name="nominalArea",
                    path="./urf:nominalArea",
                    datatype="double",
                ),
                Attribute(
                    name="prefecture",
                    path="./urf:prefecture",
                    datatype="string",
                    predefined_codelist="Common_prefecture",
                ),
                Attribute(
                    name="city",
                    path="./urf:city",
                    datatype="string",
                    predefined_codelist="Common_localPublicAuthorities",
                ),
                Attribute(
                    name="reference",
                    path="./urf:reference",
                    datatype="string",
                ),
                Attribute(
                    name="reason",
                    path="./urf:reason",
                    datatype="string",
                ),
                Attribute(
                    name="note",
                    path="./urf:note",
                    datatype="string",
                ),
                Attribute(
                    name="location",
                    path="./urf:location",
                    datatype="string",
                ),
            ],
        ),
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="areaClassificationType",
                    path="./urf:areaClassificationType",
                    datatype="string",
                    predefined_codelist="Common_areaClassificationType",
                ),
                Attribute(
                    name="urbanPlanType",
                    path="./urf:urbanPlanType",
                    datatype="string",
                    predefined_codelist="Common_urbanPlanType",
                ),
                Attribute(
                    name="areaInTotal",
                    path="./urf:areaInTotal",
                    datatype="double",
                ),
                Attribute(
                    name="number",
                    path="./urf:number",
                    datatype="string",
                ),
            ],
        ),
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="areaClassification",
                    path="./urf:areaClassification",
                    datatype="string",
                    predefined_codelist="Common_availabilityType",
                ),
                Attribute(
                    name="activityRestrictionInFarmland",
                    path="./urf:activityRestrictionInFarmland",
                    datatype="string",
                ),
                Attribute(
                    name="buildingCoverageRate",
                    path="./urf:buildingCoverageRate",
                    datatype="double",
                ),
                Attribute(
                    name="buildingDesignRestriction",
                    path="./urf:buildingDesignRestriction",
                    datatype="string",
                ),
                Attribute(
                    name="buildingLotDevelopment",
                    path="./urf:buildingLotDevelopment",
                    datatype="string",
                ),
                Attribute(
                    name="buildingRestrictions",
                    path="./urf:buildingRestrictions",
                    datatype="string",
                ),
                Attribute(
                    name="buildingUsage",
                    path="./urf:buildingUsage",
                    datatype="string",
                ),
                Attribute(
                    name="cityPopulation",
                    path="./urf:cityPopulation",
                    datatype="integer",
                ),
                Attribute(
                    name="developer",
                    path="./urf:developer",
                    datatype="string",
                ),
                Attribute(
                    name="developmentPlan",
                    path="./urf:developmentPlan",
                    datatype="string",
                ),
                Attribute(
                    name="developmentPolicy",
                    path="./urf:developmentPolicy",
                    datatype="string",
                ),
                Attribute(
                    name="disasterPreventionPublicFacilityAllocation",
                    path="./urf:disasterPreventionPublicFacilityAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="distributionBusinessPark",
                    path="./urf:distributionBusinessPark",
                    datatype="string",
                ),
                Attribute(
                    name="districtFacilitiesAllocation",
                    path="./urf:districtFacilitiesAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="districtsAllocation",
                    path="./urf:districtsAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="emergencyRecoveryPolicy",
                    path="./urf:emergencyRecoveryPolicy",
                    datatype="string",
                ),
                Attribute(
                    name="enactmentFiscalYear",
                    path="./urf:enactmentFiscalYear",
                    datatype="integer",
                ),
                Attribute(
                    name="endLocation",
                    path="./urf:endLocation",
                    datatype="string",
                ),
                Attribute(
                    name="expirationDate",
                    path="./urf:expirationDate",
                    datatype="date",
                ),
                Attribute(
                    name="facilitiesAllocation",
                    path="./urf:facilitiesAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="facilityAllocation",
                    path="./urf:facilityAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="facilityType",
                    path="./urf:facilityType",
                    datatype="string",
                    predefined_codelist="ZonalDisasterPreventionFacility_facilityType",  # ???
                ),
                Attribute(
                    name="floorAreaRate",
                    path="./urf:floorAreaRate",
                    datatype="double",
                ),
                Attribute(
                    name="guidelinePublicationDate",
                    path="./urf:guidelinePublicationDate",
                    datatype="date",
                ),
                Attribute(
                    name="housing",
                    path="./urf:housing",
                    datatype="string",
                ),
                Attribute(
                    name="housingFacilities",
                    path="./urf:housingFacilities",
                    datatype="string",
                ),
                Attribute(
                    name="housingTarget",
                    path="./urf:housingTarget",
                    datatype="string",
                ),
                Attribute(
                    name="implementationBody",
                    path="./urf:implementationBody",
                    datatype="string",
                ),
                Attribute(
                    name="implementationPeriod",
                    path="./urf:implementationPeriod",
                    datatype="string",
                ),
                Attribute(
                    name="landForCentralPublicFacilities",
                    path="./urf:landForCentralPublicFacilities",
                    datatype="string",
                ),
                Attribute(
                    name="landUsePlan",
                    path="./urf:landUsePlan",
                    datatype="string",
                ),
                Attribute(
                    name="landUsePolicy",
                    path="./urf:landUsePolicy",
                    datatype="string",
                ),
                Attribute(
                    name="landuseRestrictions",
                    path="./urf:landuseRestrictions",
                    datatype="string",
                ),
                Attribute(
                    name="maximumBuildingCoverageRate",
                    path="./urf:maximumBuildingCoverageRate",
                    datatype="double",
                ),
                Attribute(
                    name="maximumBuildingHeight",
                    path="./urf:maximumBuildingHeight",
                    datatype="string",
                ),
                Attribute(
                    name="maximumFloorAreaRate",
                    path="./urf:maximumFloorAreaRate",
                    datatype="double",
                ),
                Attribute(
                    name="minimumFloorAreaRate",
                    path="./urf:minimumFloorAreaRate",
                    datatype="double",
                ),
                Attribute(
                    name="minimumFrontageRate",
                    path="./urf:minimumFrontageRate",
                    datatype="double",
                ),
                Attribute(
                    name="minimumGreeningRate",
                    path="./urf:minimumGreeningRate",
                    datatype="double",
                ),
                Attribute(
                    name="numberOfHighRiseHousing",
                    path="./urf:numberOfHighRiseHousing",
                    datatype="integer",
                ),
                Attribute(
                    name="numberOfHousing",
                    path="./urf:numberOfHousing",
                    datatype="integer",
                ),
                Attribute(
                    name="numberOfLowRiseHousing",
                    path="./urf:numberOfLowRiseHousing",
                    datatype="integer",
                ),
                Attribute(
                    name="numberOfMiddleRiseHousing",
                    path="./urf:numberOfMiddleRiseHousing",
                    datatype="integer",
                ),
                Attribute(
                    name="objectives",
                    path="./urf:objectives",
                    datatype="string",
                ),
                Attribute(
                    name="otherPublicFacilityAllocation",
                    path="./urf:otherPublicFacilityAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="otherRestrictions",
                    path="./urf:otherRestrictions",
                    datatype="string",
                ),
                Attribute(
                    name="plan",
                    path="./urf:plan",
                    datatype="string",
                ),
                Attribute(
                    name="plannedProjectType",
                    path="./urf:plannedProjectType",
                    datatype="string",
                    predefined_codelist="UrbanDevelopmentProject_function",
                ),
                Attribute(
                    name="policy",
                    path="./urf:policy",
                    datatype="string",
                ),
                Attribute(
                    name="policyForAreaClassification",
                    path="./urf:policyForAreaClassification",
                    datatype="string",
                ),
                Attribute(
                    name="policyForUrbanPlanDecision",
                    path="./urf:policyForUrbanPlanDecision",
                    datatype="string",
                ),
                Attribute(
                    name="population",
                    path="./urf:population",
                    datatype="integer",
                ),
                Attribute(
                    name="publicAndUtilityFacilities",
                    path="./urf:publicAndUtilityFacilities",
                    datatype="string",
                ),
                Attribute(
                    name="publicFacilities",
                    path="./urf:publicFacilities",
                    datatype="string",
                ),
                Attribute(
                    name="publicFacilitiesAllocationPolicy",
                    path="./urf:publicFacilitiesAllocationPolicy",
                    datatype="string",
                ),
                Attribute(
                    name="publicFacilitiesPlans",
                    path="./urf:publicFacilitiesPlans",
                    datatype="string",
                ),
                Attribute(
                    name="publicFacilityAllocation",
                    path="./urf:publicFacilityAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="purposeForUrbanPlan",
                    path="./urf:purposeForUrbanPlan",
                    datatype="string",
                ),
                Attribute(
                    name="reasonForAreaClassification",
                    path="./urf:reasonForAreaClassification",
                    datatype="string",
                ),
                Attribute(
                    name="requirement",
                    path="./urf:requirement",
                    datatype="string",
                    predefined_codelist="SpecialGreenSpaceConservationDistrict_requirement",  # ???
                ),
                Attribute(
                    name="residentialLandUsePlan",
                    path="./urf:residentialLandUsePlan",
                    datatype="string",
                ),
                Attribute(
                    name="roadsideDistrictFacilitiesAllocation",
                    path="./urf:roadsideDistrictFacilitiesAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="ruralDistrictFacilitiesAllocation",
                    path="./urf:ruralDistrictFacilitiesAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="scheduledExecutor",
                    path="./urf:scheduledExecutor",
                    datatype="string",
                ),
                Attribute(
                    name="setbackRestrictions",
                    path="./urf:setbackRestrictions",
                    datatype="string",
                ),
                Attribute(
                    name="setbackSize",
                    path="./urf:setbackSize",
                    datatype="string",
                ),
                Attribute(
                    name="shadeRegulation",
                    path="./urf:shadeRegulation",
                    datatype="string",
                ),
                Attribute(
                    name="specificUtilityAndPublicFacilities",
                    path="./urf:specificUtilityAndPublicFacilities",
                    datatype="string",
                ),
                Attribute(
                    name="specification",
                    path="./urf:specification",
                    datatype="string",
                    predefined_codelist="Common_availabilityType",
                ),
                Attribute(
                    name="specifiedZonalDisasterPreventionFacilitiesAllocation",
                    path="./urf:specifiedZonalDisasterPreventionFacilitiesAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="startLocation",
                    path="./urf:startLocation",
                    datatype="string",
                ),
                Attribute(
                    name="storeysAboveGround",
                    path="./urf:storeysAboveGround",
                    datatype="integer",
                ),
                Attribute(
                    name="storeysBelowGround",
                    path="./urf:storeysBelowGround",
                    datatype="integer",
                ),
                Attribute(
                    name="structure",
                    path="./urf:structure",
                    datatype="string",
                    predefined_codelist="Waterway_structure",
                ),
                Attribute(
                    name="supecificBusinessFacilities",
                    path="./urf:supecificBusinessFacilities",
                    datatype="string",
                ),
                Attribute(
                    name="totalNumberOfHousing",
                    path="./urf:totalNumberOfHousing",
                    datatype="integer",
                ),
                Attribute(
                    name="unitArea",
                    path="./urf:unitArea",
                    datatype="string",
                ),
                Attribute(
                    name="urbanGreenSpaceConservation",
                    path="./urf:urbanGreenSpaceConservation",
                    datatype="string",
                ),
                Attribute(
                    name="useToBeInduced",
                    path="./urf:useToBeInduced",
                    datatype="string",
                ),
                Attribute(
                    name="utilityFacilities",
                    path="./urf:utilityFacilities",
                    datatype="string",
                ),
                Attribute(
                    name="viaLocations",
                    path="./urf:viaLocations",
                    datatype="string",
                ),
                Attribute(
                    name="wallSetbackDistance",
                    path="./urf:wallSetbackDistance",
                    datatype="string",
                ),
                Attribute(
                    name="zonalDisasterPreventionFacilitiesAllocation",
                    path="./urf:zonalDisasterPreventionFacilitiesAllocation",
                    datatype="string",
                ),
                Attribute(
                    name="zoneNumber",
                    path="./urf:zoneNumber",
                    datatype="string",
                ),
                # TODO: 入れ子データ系どうするか
                # Property(
                #    name="boundary",
                #    path="./urf:boundary",
                #    datatype="[]urf:BoundaryPropertyType",
                # ),
                # Property(
                #    name="developmentProject",
                #    path="./urf:developmentProject",
                #    datatype="[]urf:GlobalHubCityDevelopmentProjectPropertyType",
                # ),
                # Property(
                #    name="district",
                #    path="./urf:district",
                #    datatype="[]urf:DistrictPropertyType",
                # ),
                # Property(
                #    name="districtDevelopmentPlan",
                #    path="./urf:districtDevelopmentPlan",
                #    datatype="[]urf:DistrictDevelopmentPlanPropertyType",
                # ),
                # Property(
                #    name="districtFacility",
                #    path="./urf:districtFacility",
                #    datatype="[]urf:DistrictFacilityPropertyType",
                # ),
                # Property(
                #    name="privateProject",
                #    path="./urf:privateProject",
                #    datatype="[]urf:PrivateUrbanRenewalProjectPlanPropertyType",
                # ),
                # Property(
                #    name="promotionDistrict",
                #    path="./urf:promotionDistrict",
                #    datatype="[]urf:PromotionDistrictPropertyType",
                # ),
                # Property(
                #    name="specialDistrict",
                #    path="./urf:specialDistrict",
                #    datatype="[]urf:SpecialUrbanRenaissanceDistrictPropertyType",
                # ),
                # Property(
                #    name="specifiedArea",
                #    path="./urf:specifiedArea",
                #    datatype="[]urf:SpecifiedUrgentUrbanRenewalAreaPropertyType",
                # ),
                # Property(
                #    name="target",
                #    path="./urf:target",
                #    datatype="[]urf:TargetPropertyType",
                # ),
                # Property(
                #    name="threeDimensionalExtent",
                #    path="./urf:threeDimensionalExtent",
                #    datatype="[]urf:ThreeDimensionalExtentPropertyType",
                # ),
                # Property(
                #    name="zonalDisasterPreventionFacilities",
                #    path="./urf:zonalDisasterPreventionFacilities",
                #    datatype="[]urf:ZonalDisasterPreventionFacilityPropertyType",
                # ),
            ],
        ),
        AttributeGroup(
            base_element="./urf:parkAttribute/urf:ParkAttribute",
            attributes=[
                Attribute(
                    name="parkTypeNumber",
                    path="./urf:parkTypeNumber",
                    datatype="string",
                    predefined_codelist="ParkAttribute_parkTypeNumber",
                ),
                Attribute(
                    name="parkSizeNumber",
                    path="./urf:parkSizeNumber",
                    datatype="string",
                    predefined_codelist="ParkAttribute_parkSizeNumber",
                ),
                Attribute(
                    name="parkSerialNumber",
                    path="./urf:parkSerialNumber",
                    datatype="string",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./urf:parkingPlaceAttribute/urf:ParkingPlaceAttribute",
            attributes=[
                Attribute(
                    name="storeysAboveGround",
                    path="./urf:storeysAboveGround",
                    datatype="integer",
                ),
                Attribute(
                    name="storeysBelowGround",
                    path="./urf:storeysBelowGround",
                    datatype="integer",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./urf:sewerSystemsAttribute/urf:SewerSystemAttribute",
            attributes=[
                Attribute(
                    name="startLocation",
                    path="./urf:startLocation",
                    datatype="string",
                ),
                Attribute(
                    name="endLocation",
                    path="./urf:endLocation",
                    datatype="string",
                ),
                Attribute(
                    name="systemType",
                    path="./urf:systemType",
                    datatype="string",
                    predefined_codelist="SewerSystemAttribute_systemType",
                ),
                Attribute(
                    name="drainageArea",
                    path="./urf:drainageArea",
                    datatype="string",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./urf:urbanRapidTransitRailroadAttribute/urf:UrbanRapidTransitRailroadAttribute",
            attributes=[
                Attribute(
                    name="structureType",
                    path="./urf:structureType",
                    datatype="string",
                    predefined_codelist="TrafficFacility_trafficFacilityStructureType",
                ),
                Attribute(
                    name="crossType",
                    path="./urf:crossType",
                    datatype="string",
                    predefined_codelist="TrafficFacility_trafficFacilityCrossingType",
                ),
                # 入れ子データ
                # Property(
                #     name="structuralDetails",
                #     path="./urf:structuralDetails",
                #     datatype="[]urf:StructureDetails",
                # ),
            ],
        ),
        AttributeGroup(
            base_element="./urf:urbanRoadAttribute/urf:UrbanRoadAttribute",
            attributes=[
                Attribute(
                    name="routeTypeNumber",
                    path="./urf:routeTypeNumber",
                    datatype="string",
                    predefined_codelist="UrbanRoadAttribute_routeTypeNumber",
                ),
                Attribute(
                    name="routeSizeNumber",
                    path="./urf:routeSizeNumber",
                    datatype="string",
                    predefined_codelist="UrbanRoadAttribute_routeSizeNumber",
                ),
                Attribute(
                    name="routeSerialNumber",
                    path="./urf:routeSerialNumber",
                    datatype="string",
                ),
                Attribute(
                    name="roadType",
                    path="./urf:roadType",
                    datatype="string",
                    predefined_codelist="UrbanRoadAttribute_roadType",
                ),
                Attribute(
                    name="numberOfLanes",
                    path="./urf:numberOfLanes",
                    datatype="integer",
                ),
                Attribute(
                    name="roadStructure",
                    path="./urf:roadStructure",
                    datatype="string",
                ),
                Attribute(
                    name="structureType",
                    path="./urf:structureType",
                    datatype="string",
                    predefined_codelist="TrafficFacility_trafficFacilityStructureType",
                ),
                Attribute(
                    name="crossType",
                    path="./urf:crossType",
                    datatype="string",
                    predefined_codelist="TrafficFacility_trafficFacilityCrossingType",
                ),
                Attribute(
                    name="trafficPlazas",
                    path="./urf:trafficPlazas",
                    datatype="string",
                    predefined_codelist="Common_availabilityType",
                ),
                # 入れ子データ
                # Property(
                #     name="structuralDetails",
                #     path="./urf:structuralDetails",
                #     datatype="[]urf:StructureDetails",
                # ),
            ],
        ),
        AttributeGroup(
            base_element="./urf:vehicleTerminalAttribute/urf:VehicleTerminalAttribute",
            attributes=[
                Attribute(
                    name="terminalType",
                    path="./urf:terminalType",
                    datatype="string",
                    predefined_codelist="VehicleTerminalAttribute_terminalType",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./urf:waterWorksAttribute/urf:WaterWorksAttribute",
            attributes=[
                Attribute(
                    name="startLocation",
                    path="./urf:startLocation",
                    datatype="string",
                ),
                Attribute(
                    name="endLocation",
                    path="./urf:endLocation",
                    datatype="string",
                ),
            ],
        ),
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(
            collect_all=[
                "./urf:lod1MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
