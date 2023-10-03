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
                predefined_codelist="Common_districtFacilityType",
            ),
            Attribute(
                name="usage",
                path="./urf:usage",
                datatype="[]string",
                predefined_codelist="UrbanFacility_function",
            ),
        ],
    ),
    *ZONE_ATTRIBUTES,
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
        id="DistrictFacility",
        name="地区施設",
        target_elements=["urf:DistrictFacility"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="RoadsideDistrictFacility",
        name="沿道地区施設",
        target_elements=["urf:RoadsideDistrictFacility"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="RuralDistrictFacility",
        name="集落施設",
        target_elements=["urf:RuralDistrictFacility"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="ZonalDisasterPreventionFacility",
        name="地区防災施設",
        target_elements=["urf:ZonalDisasterPreventionFacility"],
        attribute_groups=[
            *_COMMON_ATTRS,
            AttributeGroup(
                base_element=None,
                attributes=[
                    Attribute(
                        name="facilityType",
                        path="./urf:facilityType",
                        datatype="string",
                        predefined_codelist="ZonalDisasterPreventionFacility_facilityType",
                    ),
                ],
            ),
        ],
        geometries=_COMMON_GEOMETRIES,
    ),
]
