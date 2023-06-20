"""Relief (dem)"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    LODDetection,
    ProcessorDefinition,
    Property,
)

RELIEF = ProcessorDefinition(
    id="ReliefFeature",
    target_elements=["dem:ReliefFeature"],
    lod_detection=LODDetection(
        lod_n="dem:lod",
    ),
    properties=[],
    emissions=FeatureEmissions(
        # NOTE: ひとまず TIN のみに対応する
        lod1=FeatureEmission(
            catch_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
        lod2=FeatureEmission(
            catch_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
        lod3=FeatureEmission(
            catch_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
    ),
)
