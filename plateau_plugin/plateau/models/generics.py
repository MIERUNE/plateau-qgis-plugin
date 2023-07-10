"""汎用都市オブジェクトモデル (./gen/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)

GENERIC_CITY_OBJECT = FeatureProcessingDefinition(
    id="gen:GenericCityObject",
    name="GenericCityObject",
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
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=[
                "./gen:lod0Geometry//gml:Polygon",
                "./gen:lod0Geometry//gml:LineString",
                # TODO: Point ?
            ],
        ),
        lod1=GeometricAttribute(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=["./gen:lod0Geometry//gml:Polygon"],
        ),
        lod2=GeometricAttribute(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=["./gen:lod0Geometry//gml:Polygon"],
        ),
        lod3=GeometricAttribute(
            lod_detection=["./gen:lod0Geometry"],
            collect_all=["./gen:lod0Geometry//gml:Polygon"],
        ),
    ),
)
