from .base import (
    Attribute,
    ChildrenPaths,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
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
    attributes=[
        Attribute(
            name="class",
            path="./wtr:class",
            datatype="string",
            codelist="WaterBody_class",
        ),
    ],
    emissions=Emissions(
        lod1=Emission(
            elem_paths=[
                "./wtr:lod1MultiSurface//gml:Polygon",
            ]
        ),
        lod2=Emission(
            elem_paths=[
                ".//wtr:lod2MultiSurface//gml:Polygon",
            ]
        ),
        lod3=Emission(
            elem_paths=[
                ".//wtr:lod3MultiSurface//gml:Polygon",
            ]
        ),
    ),
    children=ChildrenPaths(
        # NOTE: 実際のデータがない
        # lod2=[
        #     ".//wtr:WaterSurface",
        #     ".//wtr:WaterGroundSurface",
        #     ".//wtr:WaterClosureSurface",
        # ],
        # lod3=[
        #     ".//wtr:WaterSurface",
        #     ".//wtr:WaterGroundSurface",
        #     ".//wtr:WaterClosureSurface",
        # ],
    ),
)
