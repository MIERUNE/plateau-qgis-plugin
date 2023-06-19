from .base import (
    Attribute,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
)

BRIDGE = ProcessorDefinition(
    id="Bridge",
    target_elements=["brid:Bridge"],
    lod_detection=LODDetection(
        lod1=["./brid:lod1Solid"],
        lod2=["./brid:lod2Solid", "./brid:lod2MultiSurface"],
        lod3=["./brid:lod3Solid", "./brid:lod3MultiSurface"],
        lod4=["./brid:lod4Solid", "./brid:lod4MultiSurface"],
    ),
    attributes=[
        Attribute(
            name="class",
            path="./brid:class",
            datatype="string",
            codelist="Bridge_class",
        ),
        Attribute(
            name="function",
            path="./brid:function",
            datatype="[]string",
            codelist="Bridge_function",
        ),
    ],
    emissions=Emissions(
        lod1=Emission(catch_all=["./brid:lod1Solid//gml:Polygon"]),
        lod2=Emission(
            catch_all=[
                ".//brid:lod2MultiSurface//gml:Polygon",
                ".//brid:lod2Geometry//gml:Polygon",
            ],
            direct=[
                "./brid:lod2MultiSurface//gml:Polygon",
                "./brid:lod2Geometry//gml:Polygon",
            ],
        ),
        lod3=Emission(
            catch_all=[
                ".//brid:lod3MultiSurface//gml:Polygon",
                ".//brid:lod3Geometry//gml:Polygon",
            ],
            direct=[
                "./brid:lod3MultiSurface//gml:Polygon",
                "./brid:lod3Geometry//gml:Polygon",
            ],
        ),
        semantic_parts=[
            ".//brid:GroundSurface",
            ".//brid:WallSurface",
            ".//brid:RoofSurface",
            ".//brid:OuterCeilingSurface",
            ".//brid:OuterFloorSurface",
            ".//brid:ClosureSurface",
            ".//brid:BridgeConstructionElement",
            ".//brid:BridgeInstallation",
        ],
    ),
)

BRIDGE_BOUNDARY_SURFACE = ProcessorDefinition(
    id="Boundary Surface",
    target_elements=[
        "brid:GroundSurface",
        "brid:WallSurface",
        "brid:RoofSurface",
        "brid:OuterCeilingSurface",
        "brid:OuterFloorSurface",
        "brid:ClosureSurface",
    ],
    attributes=[],
    lod_detection=LODDetection(
        lod2=["./brid:lod2MultiSurface"],
        lod3=["./brid:lod3MultiSurface"],
        lod4=["./brid:lod4MultiSurface"],
    ),
    emissions=Emissions(
        lod2=Emission(
            catch_all=[
                ".//brid:lod2MultiSurface//gml:Polygon",
                ".//brid:lod2Geometry//gml:Polygon",
            ]
        ),
        lod3=Emission(
            catch_all=[
                ".//brid:lod3MultiSurface//gml:Polygon",
                ".//brid:lod3Geometry//gml:Polygon",
            ]
        ),
        lod4=Emission(
            catch_all=[
                ".//brid:lod4MultiSurface//gml:Polygon",
                ".//brid:lod4Geometry//gml:Polygon",
            ]
        ),
    ),
)

BRIDGE_CONSTRUCTION_ELEMENT = ProcessorDefinition(
    id="Construction Element",
    target_elements=[
        "brid:BridgeConstructionElement",
    ],
    attributes=[],
    lod_detection=LODDetection(
        lod2=["./brid:lod2Geometry"],
        lod3=["./brid:lod3Geometry"],
        lod4=["./brid:lod4Geometry"],
    ),
    emissions=Emissions(
        lod2=Emission(catch_all=[".//brid:lod2Geometry//gml:Polygon"]),
        lod3=Emission(catch_all=[".//brid:lod3Geometry//gml:Polygon"]),
        lod4=Emission(catch_all=[".//brid:lod4Geometry//gml:Polygon"]),
    ),
)

BRIDGE_INSTALLATION = ProcessorDefinition(
    id="Installation",
    target_elements=[
        "brid:BridgeInstallation",
    ],
    attributes=[],
    lod_detection=LODDetection(
        lod2=["./brid:lod2Geometry"],
        lod3=["./brid:lod3Geometry"],
        lod4=["./brid:lod4Geometry"],
    ),
    emissions=Emissions(
        lod2=Emission(catch_all=[".//brid:lod2Geometry//gml:Polygon"]),
        lod3=Emission(catch_all=[".//brid:lod3Geometry//gml:Polygon"]),
        lod4=Emission(catch_all=[".//brid:lod4Geometry//gml:Polygon"]),
    ),
)
