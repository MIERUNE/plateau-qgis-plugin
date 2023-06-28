"""土地利用モデル (./luse/)"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
    Property,
    PropertyGroup,
)
from .common import facility_id_attribute_attrs

LAND_USE = FeatureProcessingDefinition(
    id="LandUse",
    target_elements=[
        "luse:LandUse",
    ],
    lod_detection=LODDetection(
        lod0=["./luse:lod0MultiSurface"],
        lod1=["./luse:lod1MultiSurface"],
    ),
    property_groups=[
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="class",
                    path="./luse:class",
                    datatype="string",
                    predefined_codelist="Common_landUseType",
                ),
                Property(
                    name="usage",
                    path="./luse:usage",
                    datatype="string",
                    predefined_codelist="LandUse_usage",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./uro:landUseDetailAttribute/uro:LandUseDetailAttribute",
            properties=[
                Property(
                    name="uro:id",
                    path="./uro:id",
                    datatype="string",
                ),
                Property(
                    name="orgLandUse",
                    path="./uro:orgLandUse",
                    datatype="string",
                ),
                Property(
                    name="nominalArea",
                    path="./uro:nominalArea",
                    datatype="double",
                ),
                Property(
                    name="ownerType",
                    path="./uro:ownerType",
                    datatype="string",
                    predefined_codelist="Common_ownerType",
                ),
                Property(
                    name="owner",
                    path="./uro:owner",
                    datatype="string",
                ),
                Property(
                    name="areaInSquareMeter",
                    path="./uro:areaInSquareMeter",
                    datatype="double",
                ),
                Property(
                    name="areaInHa",
                    path="./uro:areaInHa",
                    datatype="double",
                ),
                Property(
                    name="buildingCoverageRate",
                    path="./uro:buildingCoverageRate",
                    datatype="double",
                ),
                Property(
                    name="floorAreaRate",
                    path="./uro:floorAreaRate",
                    datatype="double",
                ),
                Property(
                    name="specifiedBuildingCoverageRate",
                    path="./uro:specifiedBuildingCoverageRate",
                    datatype="double",
                ),
                Property(
                    name="specifiedFloorAreaRate",
                    path="./uro:specifiedFloorAreaRate",
                    datatype="double",
                ),
                Property(
                    name="standardFloorAreaRate",
                    path="./uro:standardFloorAreaRate",
                    datatype="double",
                ),
                Property(
                    name="urbanPlanType",
                    path="./uro:urbanPlanType",
                    datatype="string",
                    predefined_codelist="Common_urbanPlanType",
                ),
                Property(
                    name="areaClassificationType",
                    path="./uro:areaClassificationType",
                    datatype="string",
                    predefined_codelist="Common_areaClassificationType",
                ),
                Property(
                    name="districtsAndZonesType",
                    path="./uro:districtsAndZonesType",
                    datatype="[]string",
                    predefined_codelist="Common_districtsAndZonesType",
                ),
                Property(
                    name="prefecture",
                    path="./uro:prefecture",
                    datatype="string",
                    predefined_codelist="Common_prefecture",
                ),
                Property(
                    name="city",
                    path="./uro:city",
                    datatype="string",
                    predefined_codelist="Common_localPublicAuthorities",
                ),
                Property(
                    name="reference",
                    path="./uro:reference",
                    datatype="string",
                ),
                Property(
                    name="note",
                    path="./uro:note",
                    datatype="string",
                ),
                Property(
                    name="surveyYear",
                    path="./uro:surveyYear",
                    datatype="integer",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./uro:luseFacilityIdAttribute/uro:FacilityIdAttribute",
            properties=facility_id_attribute_attrs,
        ),
        # TODO: uro:luseFacilityTypeAttribute (入れ子)
        # PropertyGroup(
        #     base_element="./uro:luseFacilityTypeAttribute/uro:FacilityTypeAttribute",
        #     properties=[
        #         Property(
        #             name="class",
        #             path="./uro:class",
        #             datatype="string",
        #             predefined_codelist=None,
        #         ),
        #         Property(
        #             name="function",
        #             path="./uro:function",
        #             datatype="[]string",
        #             predefined_codelist=None,
        #         ),
        #     ],
        # ),
        # TODO: uro:luseFacilityAttribute
        # TODO: uro:luseDmAttribute (?)
    ],
    emissions=FeatureEmissions(
        lod0=FeatureEmission(
            collect_all=[
                "./luse:lod0MultiSurface//gml:Polygon",
            ]
        ),
        lod1=FeatureEmission(
            collect_all=[
                "./luse:lod1MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
