from .base import (
    FeatureEmission,
    FeatureEmissions,
    LODDetection,
    ProcessorDefinition,
    Property,
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
    properties=[
        Property(
            name="usage",
            path="./bldg:usage",
            datatype="[]string",
            codelist="Building_usage",
        ),
        Property(
            name="yearOfConstruction",
            path="./bldg:yearOfConstruction",
            datatype="integer",
        ),
        Property(
            name="yearOfDemolition",
            path="./bldg:yearOfDemolition",
            datatype="integer",
        ),
        Property(
            name="roofType",
            path="./bldg:roofType",
            datatype="string",
            codelist="Building_roofType",
        ),
        Property(
            name="measuredHeight",
            path="./bldg:measuredHeight",
            datatype="double",
        ),
        Property(
            name="storeysAboveGround",
            path="./bldg:storeysAboveGround",
            datatype="integer",
        ),
        Property(
            name="storeysBelowGround",
            path="./bldg:storeysBelowGround",
            datatype="integer",
        ),
        # Property(
        #     name="address",
        #     path="./bldg:address",
        #     datatype="string",  # xAL をどう読むか
        # ),
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(catch_all=[".//bldg:lod1Solid//gml:Polygon"]),
        lod2=FeatureEmission(
            catch_all=[".//bldg:lod2MultiSurface//gml:Polygon"],
            direct=["./bldg:lod2MultiSurface//gml:Polygon"],
        ),
        lod3=FeatureEmission(
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
    id="bldg:_BoundarySurface",
    target_elements=[
        "bldg:GroundSurface",
        "bldg:WallSurface",
        "bldg:RoofSurface",
        "bldg:OuterCeilingSurface",
        "bldg:OuterFloorSurface",
        "bldg:ClosureSurface",
    ],
    properties=[],
    lod_detection=LODDetection(
        lod2=["./bldg:lod2MultiSurface"],
        lod3=["./bldg:lod3MultiSurface"],
        lod4=["./bldg:lod4MultiSurface"],
    ),
    emissions=FeatureEmissions(
        lod2=FeatureEmission(catch_all=[".//bldg:lod2MultiSurface//gml:Polygon"]),
        lod3=FeatureEmission(catch_all=[".//bldg:lod3MultiSurface//gml:Polygon"]),
        lod4=FeatureEmission(catch_all=[".//bldg:lod4MultiSurface//gml:Polygon"]),
    ),
)
