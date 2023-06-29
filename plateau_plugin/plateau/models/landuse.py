"""土地利用モデル (./luse/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
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
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./luse:class",
                    datatype="string",
                    predefined_codelist="Common_landUseType",
                ),
                Attribute(
                    name="usage",
                    path="./luse:usage",
                    datatype="string",
                    predefined_codelist="LandUse_usage",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./uro:landUseDetailAttribute/uro:LandUseDetailAttribute",
            attributes=[
                Attribute(
                    name="uro:id",
                    path="./uro:id",
                    datatype="string",
                ),
                Attribute(
                    name="orgLandUse",
                    path="./uro:orgLandUse",
                    datatype="string",
                ),
                Attribute(
                    name="nominalArea",
                    path="./uro:nominalArea",
                    datatype="double",
                ),
                Attribute(
                    name="ownerType",
                    path="./uro:ownerType",
                    datatype="string",
                    predefined_codelist="Common_ownerType",
                ),
                Attribute(
                    name="owner",
                    path="./uro:owner",
                    datatype="string",
                ),
                Attribute(
                    name="areaInSquareMeter",
                    path="./uro:areaInSquareMeter",
                    datatype="double",
                ),
                Attribute(
                    name="areaInHa",
                    path="./uro:areaInHa",
                    datatype="double",
                ),
                Attribute(
                    name="buildingCoverageRate",
                    path="./uro:buildingCoverageRate",
                    datatype="double",
                ),
                Attribute(
                    name="floorAreaRate",
                    path="./uro:floorAreaRate",
                    datatype="double",
                ),
                Attribute(
                    name="specifiedBuildingCoverageRate",
                    path="./uro:specifiedBuildingCoverageRate",
                    datatype="double",
                ),
                Attribute(
                    name="specifiedFloorAreaRate",
                    path="./uro:specifiedFloorAreaRate",
                    datatype="double",
                ),
                Attribute(
                    name="standardFloorAreaRate",
                    path="./uro:standardFloorAreaRate",
                    datatype="double",
                ),
                Attribute(
                    name="urbanPlanType",
                    path="./uro:urbanPlanType",
                    datatype="string",
                    predefined_codelist="Common_urbanPlanType",
                ),
                Attribute(
                    name="areaClassificationType",
                    path="./uro:areaClassificationType",
                    datatype="string",
                    predefined_codelist="Common_areaClassificationType",
                ),
                Attribute(
                    name="districtsAndZonesType",
                    path="./uro:districtsAndZonesType",
                    datatype="[]string",
                    predefined_codelist="Common_districtsAndZonesType",
                ),
                Attribute(
                    name="prefecture",
                    path="./uro:prefecture",
                    datatype="string",
                    predefined_codelist="Common_prefecture",
                ),
                Attribute(
                    name="city",
                    path="./uro:city",
                    datatype="string",
                    predefined_codelist="Common_localPublicAuthorities",
                ),
                Attribute(
                    name="reference",
                    path="./uro:reference",
                    datatype="string",
                ),
                Attribute(
                    name="note",
                    path="./uro:note",
                    datatype="string",
                ),
                Attribute(
                    name="surveyYear",
                    path="./uro:surveyYear",
                    datatype="integer",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./uro:luseFacilityIdAttribute/uro:FacilityIdAttribute",
            attributes=facility_id_attribute_attrs,
        ),
        # TODO: uro:luseFacilityTypeAttribute (入れ子)
        # PropertyGroup(
        #     base_element="./uro:luseFacilityTypeAttribute/uro:FacilityTypeAttribute",
        #     attributes=[
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
