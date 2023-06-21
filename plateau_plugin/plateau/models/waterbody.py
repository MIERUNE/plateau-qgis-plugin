"""水辺モデル および 災害リスク (浸水) モデル"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    LODDetection,
    ProcessorDefinition,
    Property,
    PropertyGroup,
)

WATER_BODY = ProcessorDefinition(
    id="WaterBody",
    target_elements=[
        "wtr:WaterBody",
    ],
    lod_detection=LODDetection(
        lod1=["./wtr:lod1MultiSurface"],
        lod2=["./wtr:lod2Solid"],
        lod3=["./wtr:lod3Solid"],
    ),
    property_groups=[
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="class",
                    path="./wtr:class",
                    datatype="string",
                    codelist="WaterBody_class",
                ),
                Property(
                    name="function",
                    path="./wtr:function",
                    datatype="[]string",
                    codelist="WaterBody_function",
                ),
            ],
        )
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(
            collect_all=[
                "./wtr:lod1MultiSurface//gml:Polygon",
            ]
        ),
        lod2=FeatureEmission(
            collect_all=[
                ".//wtr:lod2MultiSurface//gml:Polygon",
            ]
        ),
        lod3=FeatureEmission(
            collect_all=[
                ".//wtr:lod3MultiSurface//gml:Polygon",
            ]
        ),
        # semantic_parts=[
        #      ".//wtr:WaterSurface",
        #      ".//wtr:WaterGroundSurface",
        #      ".//wtr:WaterClosureSurface",
        # ]
    ),
)
