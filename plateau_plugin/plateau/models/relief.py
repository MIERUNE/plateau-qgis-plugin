"""地形モデル"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    LODDetection,
    ProcessorDefinition,
    Property,
    PropertyGroup,
)

RELIEF = ProcessorDefinition(
    id="ReliefFeature",
    target_elements=["dem:ReliefFeature"],
    lod_detection=LODDetection(
        lod_n="dem:lod",
    ),
    property_groups=[],
    emissions=FeatureEmissions(
        # NOTE: ひとまず TIN のみに対応する
        lod1=FeatureEmission(
            collect_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
        lod2=FeatureEmission(
            collect_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
        lod3=FeatureEmission(
            collect_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
    ),
)
