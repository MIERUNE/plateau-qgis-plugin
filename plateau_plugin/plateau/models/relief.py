"""地形モデル (./dem/)"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
)

RELIEF = FeatureProcessingDefinition(
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
