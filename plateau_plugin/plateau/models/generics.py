"""汎用都市オブジェクトモデル (./gen/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
)

GENERIC_CITY_OBJECT = FeatureProcessingDefinition(
    id="GenericCityObject",
    target_elements=["gen:GenericCityObject"],
    load_generic_attributes=True,
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./gen:class",
                    datatype="string",
                ),
                Attribute(
                    name="function",
                    path="./gen:function",
                    datatype="[]string",
                ),
                Attribute(
                    name="usage",
                    path="./gen:usage",
                    datatype="[]string",
                ),
            ],
        )
    ],
    emissions=FeatureEmissions(
        lod0=FeatureEmission(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=[
                "./gen:lod0Geometry//gml:Polygon",
                "./gen:lod0Geometry//gml:LineString",
            ],
        ),
        lod1=FeatureEmission(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=["./gen:lod0Geometry//gml:Polygon"],
        ),
        lod2=FeatureEmission(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=["./gen:lod0Geometry//gml:Polygon"],
        ),
        lod3=FeatureEmission(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=["./gen:lod0Geometry//gml:Polygon"],
        ),
    ),
)
