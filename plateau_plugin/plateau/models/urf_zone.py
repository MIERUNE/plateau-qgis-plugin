"""区域モデル (./area/)、都市計画決定情報モデル (./urf/)"""

# TODO: 都市計画決定情報の大分類にもとづいてレイヤを分けるのがよいか?
# 現状は、都市計画決定情報の全地物を1つのレイヤにまとめている

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
    Property,
    PropertyGroup,
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
    property_groups=[
        # properties inherited from urf:Zone
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="function",
                    path="./urf:function",
                    datatype="[]string",
                    predefined_codelist=None,
                ),
                Property(
                    name="usage",
                    path="./urf:usage",
                    datatype="[]string",
                    predefined_codelist=None,
                ),
                Property(
                    name="validFrom",
                    path="./urf:validFrom",
                    datatype="date",
                ),
                Property(
                    name="validFromType",
                    path="./urf:validFromType",
                    datatype="string",
                    predefined_codelist="Common_validType",
                ),
                Property(
                    name="validTo",
                    path="./urf:validTo",
                    datatype="date",
                ),
                Property(
                    name="validToType",
                    path="./urf:validToType",
                    datatype="string",
                    predefined_codelist="Common_validType",
                ),
                Property(
                    name="expirationFiscalYear",
                    path="./urf:expirationFiscalYear",
                    datatype="integer",
                ),
                Property(
                    name="legalGrounds",
                    path="./urf:legalGrounds",
                    datatype="string",
                ),
                Property(
                    name="custodian",
                    path="./urf:custodian",
                    datatype="string",
                ),
                Property(
                    name="notificationNumber",
                    path="./urf:notificationNumber",
                    datatype="string",
                ),
                Property(
                    name="nominalArea",
                    path="./urf:nominalArea",
                    datatype="double",
                ),
                Property(
                    name="prefecture",
                    path="./urf:prefecture",
                    datatype="string",
                    predefined_codelist="Common_prefecture",
                ),
                Property(
                    name="city",
                    path="./urf:city",
                    datatype="string",
                    predefined_codelist="Common_localPublicAuthorities",
                ),
                Property(
                    name="reference",
                    path="./urf:reference",
                    datatype="string",
                ),
                Property(
                    name="reason",
                    path="./urf:reason",
                    datatype="string",
                ),
                Property(
                    name="note",
                    path="./urf:note",
                    datatype="string",
                ),
                Property(
                    name="location",
                    path="./urf:location",
                    datatype="string",
                ),
            ],
        ),
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="areaClassificationType",
                    path="./urf:areaClassificationType",
                    datatype="string",
                    predefined_codelist="Common_areaClassificationType",
                ),
                Property(
                    name="urbanPlanType",
                    path="./urf:urbanPlanType",
                    datatype="string",
                    predefined_codelist="Common_urbanPlanType",
                ),
                Property(
                    name="areaInTotal",
                    path="./urf:areaInTotal",
                    datatype="double",
                ),
                Property(
                    name="number",
                    path="./urf:number",
                    datatype="string",
                ),
            ],
        ),
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="areaClassification",
                    path="./urf:areaClassification",
                    datatype="string",
                    predefined_codelist="Common_availabilityType",
                ),
                Property(
                    name="activityRestrictionInFarmland",
                    path="./urf:activityRestrictionInFarmland",
                    datatype="string",
                ),
                Property(
                    name="buildingCoverageRate",
                    path="./urf:buildingCoverageRate",
                    datatype="double",
                ),
                Property(
                    name="buildingDesignRestriction",
                    path="./urf:buildingDesignRestriction",
                    datatype="string",
                ),
                Property(
                    name="buildingLotDevelopment",
                    path="./urf:buildingLotDevelopment",
                    datatype="string",
                ),
                Property(
                    name="buildingRestrictions",
                    path="./urf:buildingRestrictions",
                    datatype="string",
                ),
                Property(
                    name="buildingUsage",
                    path="./urf:buildingUsage",
                    datatype="string",
                ),
                Property(
                    name="cityPopulation",
                    path="./urf:cityPopulation",
                    datatype="integer",
                ),
                Property(
                    name="developer",
                    path="./urf:developer",
                    datatype="string",
                ),
                Property(
                    name="developmentPlan",
                    path="./urf:developmentPlan",
                    datatype="string",
                ),
                Property(
                    name="developmentPolicy",
                    path="./urf:developmentPolicy",
                    datatype="string",
                ),
                Property(
                    name="disasterPreventionPublicFacilityAllocation",
                    path="./urf:disasterPreventionPublicFacilityAllocation",
                    datatype="string",
                ),
                Property(
                    name="distributionBusinessPark",
                    path="./urf:distributionBusinessPark",
                    datatype="string",
                ),
                Property(
                    name="districtFacilitiesAllocation",
                    path="./urf:districtFacilitiesAllocation",
                    datatype="string",
                ),
                Property(
                    name="districtsAllocation",
                    path="./urf:districtsAllocation",
                    datatype="string",
                ),
                Property(
                    name="emergencyRecoveryPolicy",
                    path="./urf:emergencyRecoveryPolicy",
                    datatype="string",
                ),
                Property(
                    name="enactmentFiscalYear",
                    path="./urf:enactmentFiscalYear",
                    datatype="integer",
                ),
                Property(
                    name="endLocation",
                    path="./urf:endLocation",
                    datatype="string",
                ),
                Property(
                    name="expirationDate",
                    path="./urf:expirationDate",
                    datatype="date",
                ),
                Property(
                    name="facilitiesAllocation",
                    path="./urf:facilitiesAllocation",
                    datatype="string",
                ),
                Property(
                    name="facilityAllocation",
                    path="./urf:facilityAllocation",
                    datatype="string",
                ),
                Property(
                    name="facilityType",
                    path="./urf:facilityType",
                    datatype="string",
                    predefined_codelist="ZonalDisasterPreventionFacility_facilityType",  # ???
                ),
                Property(
                    name="floorAreaRate",
                    path="./urf:floorAreaRate",
                    datatype="double",
                ),
                Property(
                    name="guidelinePublicationDate",
                    path="./urf:guidelinePublicationDate",
                    datatype="date",
                ),
                Property(
                    name="housing",
                    path="./urf:housing",
                    datatype="string",
                ),
                Property(
                    name="housingFacilities",
                    path="./urf:housingFacilities",
                    datatype="string",
                ),
                Property(
                    name="housingTarget",
                    path="./urf:housingTarget",
                    datatype="string",
                ),
                Property(
                    name="implementationBody",
                    path="./urf:implementationBody",
                    datatype="string",
                ),
                Property(
                    name="implementationPeriod",
                    path="./urf:implementationPeriod",
                    datatype="string",
                ),
                Property(
                    name="landForCentralPublicFacilities",
                    path="./urf:landForCentralPublicFacilities",
                    datatype="string",
                ),
                Property(
                    name="landUsePlan",
                    path="./urf:landUsePlan",
                    datatype="string",
                ),
                Property(
                    name="landUsePolicy",
                    path="./urf:landUsePolicy",
                    datatype="string",
                ),
                Property(
                    name="landuseRestrictions",
                    path="./urf:landuseRestrictions",
                    datatype="string",
                ),
                Property(
                    name="maximumBuildingCoverageRate",
                    path="./urf:maximumBuildingCoverageRate",
                    datatype="double",
                ),
                Property(
                    name="maximumBuildingHeight",
                    path="./urf:maximumBuildingHeight",
                    datatype="string",
                ),
                Property(
                    name="maximumFloorAreaRate",
                    path="./urf:maximumFloorAreaRate",
                    datatype="double",
                ),
                Property(
                    name="minimumFloorAreaRate",
                    path="./urf:minimumFloorAreaRate",
                    datatype="double",
                ),
                Property(
                    name="minimumFrontageRate",
                    path="./urf:minimumFrontageRate",
                    datatype="double",
                ),
                Property(
                    name="minimumGreeningRate",
                    path="./urf:minimumGreeningRate",
                    datatype="double",
                ),
                Property(
                    name="numberOfHighRiseHousing",
                    path="./urf:numberOfHighRiseHousing",
                    datatype="integer",
                ),
                Property(
                    name="numberOfHousing",
                    path="./urf:numberOfHousing",
                    datatype="integer",
                ),
                Property(
                    name="numberOfLowRiseHousing",
                    path="./urf:numberOfLowRiseHousing",
                    datatype="integer",
                ),
                Property(
                    name="numberOfMiddleRiseHousing",
                    path="./urf:numberOfMiddleRiseHousing",
                    datatype="integer",
                ),
                Property(
                    name="objectives",
                    path="./urf:objectives",
                    datatype="string",
                ),
                Property(
                    name="otherPublicFacilityAllocation",
                    path="./urf:otherPublicFacilityAllocation",
                    datatype="string",
                ),
                Property(
                    name="otherRestrictions",
                    path="./urf:otherRestrictions",
                    datatype="string",
                ),
                Property(
                    name="plan",
                    path="./urf:plan",
                    datatype="string",
                ),
                Property(
                    name="plannedProjectType",
                    path="./urf:plannedProjectType",
                    datatype="string",
                    predefined_codelist="UrbanDevelopmentProject_function",
                ),
                Property(
                    name="policy",
                    path="./urf:policy",
                    datatype="string",
                ),
                Property(
                    name="policyForAreaClassification",
                    path="./urf:policyForAreaClassification",
                    datatype="string",
                ),
                Property(
                    name="policyForUrbanPlanDecision",
                    path="./urf:policyForUrbanPlanDecision",
                    datatype="string",
                ),
                Property(
                    name="population",
                    path="./urf:population",
                    datatype="integer",
                ),
                Property(
                    name="publicAndUtilityFacilities",
                    path="./urf:publicAndUtilityFacilities",
                    datatype="string",
                ),
                Property(
                    name="publicFacilities",
                    path="./urf:publicFacilities",
                    datatype="string",
                ),
                Property(
                    name="publicFacilitiesAllocationPolicy",
                    path="./urf:publicFacilitiesAllocationPolicy",
                    datatype="string",
                ),
                Property(
                    name="publicFacilitiesPlans",
                    path="./urf:publicFacilitiesPlans",
                    datatype="string",
                ),
                Property(
                    name="publicFacilityAllocation",
                    path="./urf:publicFacilityAllocation",
                    datatype="string",
                ),
                Property(
                    name="purposeForUrbanPlan",
                    path="./urf:purposeForUrbanPlan",
                    datatype="string",
                ),
                Property(
                    name="reasonForAreaClassification",
                    path="./urf:reasonForAreaClassification",
                    datatype="string",
                ),
                Property(
                    name="requirement",
                    path="./urf:requirement",
                    datatype="string",
                    predefined_codelist="SpecialGreenSpaceConservationDistrict_requirement",  # ???
                ),
                Property(
                    name="residentialLandUsePlan",
                    path="./urf:residentialLandUsePlan",
                    datatype="string",
                ),
                Property(
                    name="roadsideDistrictFacilitiesAllocation",
                    path="./urf:roadsideDistrictFacilitiesAllocation",
                    datatype="string",
                ),
                Property(
                    name="ruralDistrictFacilitiesAllocation",
                    path="./urf:ruralDistrictFacilitiesAllocation",
                    datatype="string",
                ),
                Property(
                    name="scheduledExecutor",
                    path="./urf:scheduledExecutor",
                    datatype="string",
                ),
                Property(
                    name="setbackRestrictions",
                    path="./urf:setbackRestrictions",
                    datatype="string",
                ),
                Property(
                    name="setbackSize",
                    path="./urf:setbackSize",
                    datatype="string",
                ),
                Property(
                    name="shadeRegulation",
                    path="./urf:shadeRegulation",
                    datatype="string",
                ),
                Property(
                    name="specificUtilityAndPublicFacilities",
                    path="./urf:specificUtilityAndPublicFacilities",
                    datatype="string",
                ),
                Property(
                    name="specification",
                    path="./urf:specification",
                    datatype="string",
                    predefined_codelist="Common_availabilityType",
                ),
                Property(
                    name="specifiedZonalDisasterPreventionFacilitiesAllocation",
                    path="./urf:specifiedZonalDisasterPreventionFacilitiesAllocation",
                    datatype="string",
                ),
                Property(
                    name="startLocation",
                    path="./urf:startLocation",
                    datatype="string",
                ),
                Property(
                    name="storeysAboveGround",
                    path="./urf:storeysAboveGround",
                    datatype="integer",
                ),
                Property(
                    name="storeysBelowGround",
                    path="./urf:storeysBelowGround",
                    datatype="integer",
                ),
                Property(
                    name="structure",
                    path="./urf:structure",
                    datatype="string",
                    predefined_codelist="Waterway_structure",
                ),
                Property(
                    name="supecificBusinessFacilities",
                    path="./urf:supecificBusinessFacilities",
                    datatype="string",
                ),
                Property(
                    name="totalNumberOfHousing",
                    path="./urf:totalNumberOfHousing",
                    datatype="integer",
                ),
                Property(
                    name="unitArea",
                    path="./urf:unitArea",
                    datatype="string",
                ),
                Property(
                    name="urbanGreenSpaceConservation",
                    path="./urf:urbanGreenSpaceConservation",
                    datatype="string",
                ),
                Property(
                    name="useToBeInduced",
                    path="./urf:useToBeInduced",
                    datatype="string",
                ),
                Property(
                    name="utilityFacilities",
                    path="./urf:utilityFacilities",
                    datatype="string",
                ),
                Property(
                    name="viaLocations",
                    path="./urf:viaLocations",
                    datatype="string",
                ),
                Property(
                    name="wallSetbackDistance",
                    path="./urf:wallSetbackDistance",
                    datatype="string",
                ),
                Property(
                    name="zonalDisasterPreventionFacilitiesAllocation",
                    path="./urf:zonalDisasterPreventionFacilitiesAllocation",
                    datatype="string",
                ),
                Property(
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
        PropertyGroup(
            base_element="./urf:parkAttribute/urf:ParkAttribute",
            properties=[
                Property(
                    name="parkTypeNumber",
                    path="./urf:parkTypeNumber",
                    datatype="string",
                    predefined_codelist="ParkAttribute_parkTypeNumber",
                ),
                Property(
                    name="parkSizeNumber",
                    path="./urf:parkSizeNumber",
                    datatype="string",
                    predefined_codelist="ParkAttribute_parkSizeNumber",
                ),
                Property(
                    name="parkSerialNumber",
                    path="./urf:parkSerialNumber",
                    datatype="string",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./urf:parkingPlaceAttribute/urf:ParkingPlaceAttribute",
            properties=[
                Property(
                    name="storeysAboveGround",
                    path="./urf:storeysAboveGround",
                    datatype="integer",
                ),
                Property(
                    name="storeysBelowGround",
                    path="./urf:storeysBelowGround",
                    datatype="integer",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./urf:sewerSystemsAttribute/urf:SewerSystemAttribute",
            properties=[
                Property(
                    name="startLocation",
                    path="./urf:startLocation",
                    datatype="string",
                ),
                Property(
                    name="endLocation",
                    path="./urf:endLocation",
                    datatype="string",
                ),
                Property(
                    name="systemType",
                    path="./urf:systemType",
                    datatype="string",
                    predefined_codelist="SewerSystemAttribute_systemType",
                ),
                Property(
                    name="drainageArea",
                    path="./urf:drainageArea",
                    datatype="string",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./urf:urbanRapidTransitRailroadAttribute/urf:UrbanRapidTransitRailroadAttribute",
            properties=[
                Property(
                    name="structureType",
                    path="./urf:structureType",
                    datatype="string",
                    predefined_codelist="TrafficFacility_trafficFacilityStructureType",
                ),
                Property(
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
        PropertyGroup(
            base_element="./urf:urbanRoadAttribute/urf:UrbanRoadAttribute",
            properties=[
                Property(
                    name="routeTypeNumber",
                    path="./urf:routeTypeNumber",
                    datatype="string",
                    predefined_codelist="UrbanRoadAttribute_routeTypeNumber",
                ),
                Property(
                    name="routeSizeNumber",
                    path="./urf:routeSizeNumber",
                    datatype="string",
                    predefined_codelist="UrbanRoadAttribute_routeSizeNumber",
                ),
                Property(
                    name="routeSerialNumber",
                    path="./urf:routeSerialNumber",
                    datatype="string",
                ),
                Property(
                    name="roadType",
                    path="./urf:roadType",
                    datatype="string",
                    predefined_codelist="UrbanRoadAttribute_roadType",
                ),
                Property(
                    name="numberOfLanes",
                    path="./urf:numberOfLanes",
                    datatype="integer",
                ),
                Property(
                    name="roadStructure",
                    path="./urf:roadStructure",
                    datatype="string",
                ),
                Property(
                    name="structureType",
                    path="./urf:structureType",
                    datatype="string",
                    predefined_codelist="TrafficFacility_trafficFacilityStructureType",
                ),
                Property(
                    name="crossType",
                    path="./urf:crossType",
                    datatype="string",
                    predefined_codelist="TrafficFacility_trafficFacilityCrossingType",
                ),
                Property(
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
        PropertyGroup(
            base_element="./urf:vehicleTerminalAttribute/urf:VehicleTerminalAttribute",
            properties=[
                Property(
                    name="terminalType",
                    path="./urf:terminalType",
                    datatype="string",
                    predefined_codelist="VehicleTerminalAttribute_terminalType",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./urf:waterWorksAttribute/urf:WaterWorksAttribute",
            properties=[
                Property(
                    name="startLocation",
                    path="./urf:startLocation",
                    datatype="string",
                ),
                Property(
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
