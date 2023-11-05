"""公共測量標準図式 (DM) を子Featureとして処理する"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)

DM_GEOMETRIC = FeatureProcessingDefinition(
    id="uro:DmGeometric",
    name="DmGeometric",
    target_elements=["uro:DmGeometricAttribute"],
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="dmCode",
                    path="./uro:dmCode",
                    datatype="string",
                    predefined_codelist="Common_dmCode",
                ),
                Attribute(
                    name="meshCode",
                    path="./uro:meshCode",
                    datatype="string",
                ),
            ],
        ),
    ],
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./uro:lod0Geometry"],
            collect_all=[
                "./uro:lod0Geometry//gml:Polygon",
                "./uro:lod0Geometry//gml:LineString",
                "./uro:lod0Geometry//gml:Point",
            ],
        ),
    ),
)
