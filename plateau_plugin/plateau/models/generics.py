from .base import (
    FeatureEmission,
    FeatureEmissions,
    LODDetection,
    ProcessorDefinition,
    Property,
    PropertyGroup,
)

GENERIC_CITY_OBJECT = ProcessorDefinition(
    id="GenericCityObject",
    target_elements=["gen:GenericCityObject"],
    lod_detection=LODDetection(
        lod0=["./gen:lod0Geometry"],
        lod1=["./gen:lod1Geometry"],
        lod2=["./gen:lod2Geometry"],
        lod3=["./gen:lod3Geometry"],
    ),
    property_groups=[],
    emissions=FeatureEmissions(
        lod0=FeatureEmission(catch_all=["./gen:lod0Geometry//gml:Polygon"]),
        lod1=FeatureEmission(catch_all=["./gen:lod1Geometry//gml:Polygon"]),
        lod2=FeatureEmission(catch_all=["./gen:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(catch_all=["./gen:lod3Geometry//gml:Polygon"]),
    ),
)
