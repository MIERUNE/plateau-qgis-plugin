"""地形モデル (./dem/)

地形モデルをベクタレイヤとして読み込む。

メッシュレイヤとして読み込むための別のアルゴリズムの使用を推奨する。
"""

from .base import (
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)

RELIEF = FeatureProcessingDefinition(
    id="dem:ReliefFeature",
    name="ReliefFeature",
    target_elements=["dem:ReliefFeature"],
    attribute_groups=[],
    geometries=GeometricAttributes(
        # TODO: ひとまず TIN のみに対応している
        lod_n="dem:lod",
        lod_n_paths=GeometricAttribute(
            lod_detection=[],
            collect_all=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"],
        ),
    ),
    dm_attr_container_path="./uro:demDmAttribute",
)
