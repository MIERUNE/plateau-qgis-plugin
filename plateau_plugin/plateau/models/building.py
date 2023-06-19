from .base import (
    Attribute,
    ChildrenPaths,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
)

BUILDING = ProcessorDefinition(
    id="Building",
    target_elements=["bldg:Building"],
    lod_detection=LODDetection(
        lod1=["./bldg:lod1Solid"],
        lod2=["./bldg:lod2Solid"],
        lod3=["./bldg:lod3Solid"],
        # lod4=["./bldg:lod4Solid", "./bldg:lod4MultiSurface"],
    ),
    attributes=[
        Attribute(
            name="usage",
            xpath="./bldg:usage/text()",
            datatype="[]string",
            codelist="Building_usage",
        ),
    ],
    emissions=Emissions(
        lod1=Emission(
            elem_paths=[
                "./bldg:lod1Solid/gml:Solid/gml:exterior/gml:CompositeSurface//gml:Polygon"
            ]
        ),
        lod2=Emission(elem_paths=["./bldg:*//bldg:lod2MultiSurface//gml:Polygon"]),
        lod3=Emission(elem_paths=["./bldg:*//bldg:lod3MultiSurface//gml:Polygon"]),
    ),
    children=ChildrenPaths(
        lod2=[
            ".//bldg:GroundSurface",
            ".//bldg:WallSurface",
            ".//bldg:RoofSurface",
            ".//bldg:OuterCeilingSurface",
            ".//bldg:OuterFloorSurface",
            ".//bldg:ClosureSurface",
        ],
        lod3=[
            ".//bldg:GroundSurface",
            ".//bldg:WallSurface",
            ".//bldg:RoofSurface",
            ".//bldg:OuterCeilingSurface",
            ".//bldg:ClosureSurface",
        ],
    ),
)

BOUNDARY_SURFACE = ProcessorDefinition(
    id="Boundary Surface",
    target_elements=[
        "bldg:GroundSurface",
        "bldg:WallSurface",
        "bldg:RoofSurface",
        "bldg:OuterCeilingSurface",
        "bldg:OuterFloorSurface",
        "bldg:ClosureSurface",
    ],
    attributes=[],
    lod_detection=LODDetection(
        lod2=["./bldg:lod2MultiSurface"],
        lod3=["./bldg:lod3MultiSurface"],
        lod4=["./bldg:lod4MultiSurface"],
    ),
    emissions=Emissions(
        lod2=Emission(elem_paths=[".//bldg:lod2MultiSurface//gml:Polygon"]),
        lod3=Emission(elem_paths=[".//bldg:lod3MultiSurface//gml:Polygon"]),
        lod4=Emission(elem_paths=[".//bldg:lod4MultiSurface//gml:Polygon"]),
    ),
)
