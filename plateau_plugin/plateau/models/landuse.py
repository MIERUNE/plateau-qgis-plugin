from .base import (
    FeatureEmission,
    FeatureEmissions,
    LODDetection,
    ProcessorDefinition,
    Property,
)

LAND_USE = ProcessorDefinition(
    id="LandUse",
    target_elements=[
        "luse:LandUse",
    ],
    lod_detection=LODDetection(
        lod1=["./luse:lod1MultiSurface"],
    ),
    properties=[
        Property(
            name="class",
            path="./luse:class",
            datatype="string",
            codelist="Common_landUseType",
        ),
        Property(
            name="usage",
            path="./luse:usage",
            datatype="string",
            codelist="LandUse_usage",
        ),
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(
            catch_all=[
                "./luse:lod1MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
