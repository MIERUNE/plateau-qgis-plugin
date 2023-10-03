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
                predefined_codelist="ScheduledAreaForUrbanDevelopment_function",
            ),
        ],
    ),
    *ZONE_ATTRIBUTES,
    AttributeGroup(
        base_element=None,
        attributes=[
            Attribute(
                name="scheduledExecutor",
                path="./urf:scheduledExecutor",
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
        id="urf:ScheduledAreaForUrbanDevelopmentProject",
        name="市街地開発事業等の予定区域",
        target_elements=["urf:ScheduledAreaForUrbanDevelopmentProject"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:ScheduledAreaForIndustrialParkDevelopmentProjects",
        name="工業団地造成事業の予定区域",
        target_elements=["urf:ScheduledAreaForIndustrialParkDevelopmentProjects"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:ScheduledAreaForNewUrbanInfrastructureProjects",
        name="新都市基盤整備事業の予定区域",
        target_elements=["urf:ScheduledAreaForNewUrbanInfrastructureProjects"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:ScheduledAreaForCollectiveHousingFacilities",
        name="一団地の住宅施設の予定区域",
        target_elements=["urf:ScheduledAreaForCollectiveHousingFacilities"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:ScheduledAreaForCollectiveGovernmentAndPublicOfficeFacilities",
        name="一団地の官公庁施設の予定区域",
        target_elements=[
            "urf:ScheduledAreaForCollectiveGovernmentAndPublicOfficeFacilities"
        ],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
    FeatureProcessingDefinition(
        id="urf:ScheduledAreaForDistributionBusinessPark",
        name="新都市基盤整備事業の予定区域",
        target_elements=["urf:ScheduledAreaForDistributionBusinessPark"],
        attribute_groups=_COMMON_ATTRS,
        geometries=_COMMON_GEOMETRIES,
    ),
]
