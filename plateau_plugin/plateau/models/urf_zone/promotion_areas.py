from ..base import (
    Attribute,
    AttributeGroup,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)
from .common import ZONE_ATTRIBUTES

_COMMON_ATTRS = [
    AttributeGroup(
        base_element=None,
        attributes=[
            Attribute(
                name="function",
                path="./urf:function",
                datatype="[]string",
                predefined_codelist="ProjectPromotionArea_function",
            ),
        ],
    ),
    *ZONE_ATTRIBUTES,
    AttributeGroup(
        base_element=None,
        attributes=[
            Attribute(
                name="developmentPolicy",
                path="./urf:developmentPolicy",
                datatype="string",
            ),
            Attribute(
                name="publicFacilitiesPlans",
                path="./urf:publicFacilitiesPlans",
                datatype="string",
            ),
        ],
    ),
]

_COMMON_GEOMETRIES = GeometricAttributes(
    lod1=GeometricAttribute(
        is2d=True,
        lod_detection=["./urf:lod1MultiSurface", "./urf:lod0MultiSurface"],
        collect_all=[
            "./urf:lod1MultiSurface//gml:Polygon",
            "./urf:lod0MultiSurface//gml:Polygon",
        ],
    ),
)

DEFS = [
    FeatureProcessingDefinition(
        id="urf:ProjectPromotionArea",
        name="ProjectPromotionArea",
        target_elements=["urf:ProjectPromotionArea"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:UrbanRedevelopmentPromotionArea",
        name="市街地再開発促進区域",
        target_elements=["urf:UrbanRedevelopmentPromotionArea"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="publicFacilities",
                        path="./urf:publicFacilities",
                        datatype="string",
                    ),
                    Attribute(
                        name="unitArea",
                        path="./urf:unitArea",
                        datatype="string",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:LandReadjustmentPromotionArea",
        name="土地区画整理促進区域",
        target_elements=["urf:LandReadjustmentPromotionArea"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:ResidentialBlockConstructionPromotionArea",
        name="住宅街区整備促進区域",
        target_elements=["urf:ResidentialBlockConstructionPromotionArea"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:LandReadjustmentPromotionAreasForCoreBusinessUrbanDevelopment",
        name="拠点業務市街地整備土地区画整理促進区域",
        target_elements=[
            "urf:LandReadjustmentPromotionAreasForCoreBusinessUrbanDevelopment"
        ],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
]
