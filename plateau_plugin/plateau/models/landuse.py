from .base import (
    Attribute,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
)

LAND_USE = ProcessorDefinition(
    id="LandUse",
    target_elements=[
        "luse:LandUse",
    ],
    lod_detection=LODDetection(
        lod1=["./luse:lod1MultiSurface"],
    ),
    attributes=[
        Attribute(
            name="class",
            path="./luse:class",
            datatype="string",
            codelist="Common_landUseType",
        ),
        Attribute(
            name="usage",
            path="./luse:usage",
            datatype="string",
            codelist="LandUse_usage",
        ),
    ],
    emissions=Emissions(
        lod1=Emission(
            catch_all=[
                "./luse:lod1MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
