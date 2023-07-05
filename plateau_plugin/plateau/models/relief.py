"""地形モデル (./dem/)"""

from .base import (
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)

RELIEF = FeatureProcessingDefinition(
    id="ReliefFeature",
    target_elements=["dem:ReliefFeature"],
    attribute_groups=[],
    geometries=GeometricAttributes(
        # TODO: ひとまず TIN のみに対応しているが...
        lod_n="dem:lod",
        lod_n_paths=GeometricAttribute(
            lod_detection=[],
            collect_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"],
        ),
    ),
    dm_attr_container_path="./uro:demDmAttribute",
)
