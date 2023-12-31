from ..base import (
    Attribute,
    AttributeGroup,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)
from .common import ZONE_ATTRIBUTES

_URF_ZONE = FeatureProcessingDefinition(
    id="urf:Zone",
    name="Zone",
    target_elements=["urf:Zone"],
    attribute_groups=ZONE_ATTRIBUTES,
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod0MultiSurface"],
            collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
        ),
        lod1=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod1MultiSurface"],
            collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
        ),
    ),
)

_URF_URBAN_PLANNING_AREA = FeatureProcessingDefinition(
    id="urf:UrbanPlanningArea",
    name="都市計画区域",
    target_elements=["urf:UrbanPlanningArea"],
    attribute_groups=[
        *ZONE_ATTRIBUTES,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="function",
                    path="./urf:function",
                    datatype="[]string",
                    predefined_codelist="Common_urbanPlanType",
                ),
                Attribute(
                    name="areaClassification",
                    path="./urf:areaClassification",
                    datatype="string",
                    predefined_codelist="Common_availabilityType",
                ),
                Attribute(
                    name="cityArea",
                    path="./urf:cityArea",
                    datatype="double",
                ),
                Attribute(
                    name="cityPopulation",
                    path="./urf:cityPopulation",
                    datatype="integer",
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
                    name="purposeForUrbanPlan",
                    path="./urf:purposeForUrbanPlan",
                    datatype="string",
                ),
                Attribute(
                    name="reasonForAreaClassification",
                    path="./urf:reasonForAreaClassification",
                    datatype="string",
                ),
            ],
        ),
    ],
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod0MultiSurface"],
            collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
        ),
        lod1=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod1MultiSurface"],
            collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
        ),
    ),
)

_URF_QUASI_URBAN_PLANNING_AREA = FeatureProcessingDefinition(
    id="urf:QuasiUrbanPlanningArea",
    name="準都市計画区域",
    target_elements=["urf:QuasiUrbanPlanningArea"],
    attribute_groups=[
        *ZONE_ATTRIBUTES,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="function",
                    path="./urf:function",
                    datatype="[]string",
                    predefined_codelist="Common_urbanPlanType",
                ),
                Attribute(
                    name="cityArea",
                    path="./urf:cityArea",
                    datatype="double",
                ),
                Attribute(
                    name="cityPopulation",
                    path="./urf:cityPopulation",
                    datatype="integer",
                ),
                Attribute(
                    name="population",
                    path="./urf:population",
                    datatype="integer",
                ),
            ],
        ),
    ],
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod0MultiSurface"],
            collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
        ),
        lod1=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod1MultiSurface"],
            collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
        ),
    ),
)

_URF_AREA_CLASSIFICATION = FeatureProcessingDefinition(
    id="urf:AreaClassification",
    name="区域区分",
    target_elements=["urf:AreaClassification"],
    attribute_groups=[
        *ZONE_ATTRIBUTES,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="function",
                    path="./urf:function",
                    datatype="[]string",
                    predefined_codelist="Common_areaClassificationType",
                ),
                Attribute(
                    name="population",
                    path="./urf:population",
                    datatype="integer",
                ),
            ],
        ),
    ],
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod0MultiSurface"],
            collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
        ),
        lod1=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod1MultiSurface"],
            collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
        ),
    ),
)

_URF_UNUSED_LAND_USE_PROMOTION_AREA = FeatureProcessingDefinition(
    id="urf:UnusedLandUsePromotionArea",
    name="遊休土地転換利用促進地区",
    target_elements=["urf:UnusedLandUsePromotionArea"],
    attribute_groups=ZONE_ATTRIBUTES,
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod0MultiSurface"],
            collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
        ),
        lod1=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod1MultiSurface"],
            collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
        ),
    ),
)

_URF_URBAN_DISASTER_RECOVERY_PROMOTION_AREA = FeatureProcessingDefinition(
    id="urf:UrbanDisasterRecoveryPromotionArea",
    name="被災市街地復興推進地域",
    target_elements=["urf:UrbanDisasterRecoveryPromotionArea"],
    attribute_groups=[
        *ZONE_ATTRIBUTES,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="emergencyRecoveryPolicy",
                    path="./urf:emergencyRecoveryPolicy",
                    datatype="string",
                ),
                Attribute(
                    name="expirationDate",
                    path="./urf:expirationDate",
                    datatype="date",
                ),
                Attribute(
                    name="plannedProjectType",
                    path="./urf:plannedProjectType",
                    datatype="string",
                    predefined_codelist="UrbanDevelopmentProject_function",
                ),
            ],
        ),
    ],
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod0MultiSurface"],
            collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
        ),
        lod1=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod1MultiSurface"],
            collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
        ),
    ),
)

_URF_PROMOTION_DISTRICT = FeatureProcessingDefinition(
    id="urf:PromotionDistrict",
    name="促進区",
    target_elements=["urf:PromotionDistrict"],
    attribute_groups=[
        *ZONE_ATTRIBUTES,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="function",
                    path="./urf:function",
                    datatype="[]string",
                    predefined_codelist="PromotionArea_function",
                ),
            ],
        ),
    ],
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod0MultiSurface"],
            collect_all=["./urf:lod0MultiSurface//gml:Polygon"],
        ),
        lod1=GeometricAttribute(
            is2d=True,
            lod_detection=["./urf:lod1MultiSurface"],
            collect_all=["./urf:lod1MultiSurface//gml:Polygon"],
        ),
    ),
)


DEFS = [
    _URF_ZONE,
    _URF_AREA_CLASSIFICATION,
    _URF_QUASI_URBAN_PLANNING_AREA,
    _URF_UNUSED_LAND_USE_PROMOTION_AREA,
    _URF_URBAN_DISASTER_RECOVERY_PROMOTION_AREA,
    _URF_URBAN_PLANNING_AREA,
    _URF_PROMOTION_DISTRICT,
]
