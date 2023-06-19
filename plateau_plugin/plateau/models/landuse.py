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
    attributes=[],
    emissions=Emissions(
        lod1=Emission(
            elem_paths=[
                "./luse:lod1MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
