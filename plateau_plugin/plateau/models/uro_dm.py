"""公共測量標準図式 (DM)"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
)

DM_GEOMETRIC = FeatureProcessingDefinition(
    id="DmGeometric",
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
    emissions=FeatureEmissions(
        lod0=FeatureEmission(
            lod_detection=["./uro:lod0Geometry"],
            collect_all=[
                "./uro:lod0Geometry//gml:Polygon",
                "./uro:lod0Geometry//gml:LineString",
                # TODO: Point ?
            ],
        ),
    ),
)
