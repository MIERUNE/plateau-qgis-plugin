from .base import (
    Attribute,
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
            path="./bldg:usage",
            datatype="[]string",
            codelist="Building_usage",
        ),
    ],
    emissions=Emissions(
        lod1=Emission(catch_all=[".//bldg:lod1Solid//gml:Polygon"]),
        lod2=Emission(
            catch_all=[".//bldg:lod2MultiSurface//gml:Polygon"],
            direct=["./bldg:lod2MultiSurface//gml:Polygon"],
        ),
        lod3=Emission(
            catch_all=[".//bldg:lod3MultiSurface//gml:Polygon"],
            direct=["./bldg:lod3MultiSurface//gml:Polygon"],
        ),
        semantic_parts=[
            ".//bldg:GroundSurface",
            ".//bldg:WallSurface",
            ".//bldg:RoofSurface",
            ".//bldg:OuterCeilingSurface",
            ".//bldg:OuterFloorSurface",
            ".//bldg:ClosureSurface",
        ],
    ),
)

BUILDING_BOUNDARY_SURFACE = ProcessorDefinition(
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
        lod2=Emission(catch_all=[".//bldg:lod2MultiSurface//gml:Polygon"]),
        lod3=Emission(catch_all=[".//bldg:lod3MultiSurface//gml:Polygon"]),
        lod4=Emission(catch_all=[".//bldg:lod4MultiSurface//gml:Polygon"]),
    ),
)
