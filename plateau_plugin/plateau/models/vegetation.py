from .base import (
    Attribute,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
)

SOLITARY_VEGETATION_OBJECT = ProcessorDefinition(
    id="SolitaryVegetationObject",
    target_elements=["veg:SolitaryVegetationObject"],
    lod_detection=LODDetection(
        lod1=["./veg:lod1Geometry"],
        lod2=["./veg:lod2Geometry"],
        lod3=["./veg:lod3Geometry"],
    ),
    attributes=[],
    emissions=Emissions(
        lod1=Emission(elem_paths=["./veg:lod1Geometry//gml:Polygon"]),
        lod2=Emission(elem_paths=["./veg:lod2Geometry//gml:Polygon"]),
        lod3=Emission(elem_paths=["./veg:lod3Geometry//gml:Polygon"]),
    ),
)

PLANT_COVER = ProcessorDefinition(
    id="PlantCover",
    target_elements=["veg:PlantCover"],
    lod_detection=LODDetection(
        lod1=["./veg:lod1MultiSolid", "./veg:lod1MultiSurface"],
        lod2=["./veg:lod2MultiSolid", "./veg:lod2MultiSurface"],
        lod3=["./veg:lod3MultiSolid", "./veg:lod3MultiSurface"],
    ),
    attributes=[],
    emissions=Emissions(
        lod1=Emission(
            elem_paths=[
                "./veg:lod1MultiSolid//gml:Polygon",
                "./veg:lod1MultiSurface//gml:Polygon",
            ]
        ),
        lod2=Emission(
            elem_paths=[
                "./veg:lod1MultiSolid//gml:Polygon",
                "./veg:lod2MultiSurface//gml:Polygon",
            ]
        ),
        lod3=Emission(
            elem_paths=[
                "./veg:lod1MultiSolid//gml:Polygon",
                "./veg:lod3MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
