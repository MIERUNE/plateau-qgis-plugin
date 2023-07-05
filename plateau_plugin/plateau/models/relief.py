"""地形モデル (./dem/)"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
)

RELIEF = FeatureProcessingDefinition(
    id="ReliefFeature",
    target_elements=["dem:ReliefFeature"],
    attribute_groups=[],
    emissions=FeatureEmissions(
        # TODO: ひとまず TIN のみに対応しているが...
        lod_n="dem:lod",
        lod_n_paths=FeatureEmission(
            lod_detection=[],
            collect_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"],
        ),
    ),
    dm_attr_container_path="./uro:demDmAttribute",
)
