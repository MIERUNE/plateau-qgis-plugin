"""その他の構造物モデル (./cons/)"""

# FIXME:
# TODO: 以下、bldg:Building 用の定義をコピペしただけなので、内容は要検証

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
    Property,
    PropertyGroup,
)


def _make_prefix_variants(prefixed_names: list[str]) -> list[str]:
    # uro を uro2, uro3 に置換する
    names = []
    for name in prefixed_names:
        assert name.startswith("uro:")
        n = name.split(":")[1]
        names.append("uro2:" + n)
        names.append("uro3:" + n)
    return names


OTHER_CONSTRUCTION = FeatureProcessingDefinition(
    id="OtherConstruction",
    target_elements=_make_prefix_variants(["uro:OtherConstruction"]),
    lod_detection=LODDetection(
        lod1=["./uro:lod1Geometry"],
        lod2=["./uro:lod2Geometry"],
        lod3=["./uro:lod3Geometry"],
    ),
    property_groups=[
        # TODO
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(collect_all=["./uro:lod1Solid//gml:Polygon"]),
        lod2=FeatureEmission(
            collect_all=[
                ".//uro:lod2MultiSurface//gml:Polygon",
                ".//uro:lod2Geometry//gml:Polygon",
            ],
            only_direct=[
                "./uro:lod2MultiSurface//gml:Polygon",
                "./uro:lod2Geometry//gml:Polygon",
            ],
        ),
        lod3=FeatureEmission(
            collect_all=[
                ".//uro:lod3MultiSurface//gml:Polygon",
                ".//uro:lod3Geometry//gml:Polygon",
            ],
            only_direct=[
                "./uro:lod3MultiSurface//gml:Polygon",
                "./uro:lod3Geometry//gml:Polygon",
            ],
        ),
        semantic_parts=[
            ".//uro:GroundSurface",
            ".//uro:WallSurface",
            ".//uro:RoofSurface",
            ".//uro:OuterCeilingSurface",
            ".//uro:OuterFloorSurface",
            ".//uro:ClosureSurface",
            ".//uro:ConstructionInstallation",
        ],
    ),
)

OTHER_CONSTRUCTION_BOUNDARY_SURFACE = FeatureProcessingDefinition(
    id="uro:_BoundarySurface",
    target_elements=_make_prefix_variants(
        [
            "uro:GroundSurface",
            "uro:WallSurface",
            "uro:RoofSurface",
            "uro:OuterCeilingSurface",
            "uro:OuterFloorSurface",
            "uro:ClosureSurface",
        ]
    ),
    property_groups=[],
    lod_detection=LODDetection(
        lod2=["./uro:lod2MultiSurface"],
        lod3=["./uro:lod3MultiSurface"],
        lod4=["./uro:lod4MultiSurface"],
    ),
    emissions=FeatureEmissions(
        lod2=FeatureEmission(
            collect_all=[
                ".//uro:lod2MultiSurface//gml:Polygon",
                ".//uro:lod2Geometry//gml:Polygon",
            ]
        ),
        lod3=FeatureEmission(
            collect_all=[
                ".//uro:lod3MultiSurface//gml:Polygon",
                ".//uro:lod3Geometry//gml:Polygon",
            ]
        ),
        lod4=FeatureEmission(
            collect_all=[
                ".//uro:lod4MultiSurface//gml:Polygon",
                ".//uro:lod4Geometry//gml:Polygon",
            ]
        ),
    ),
)

OTHER_CONSTRUCTION_INSTALLATION = FeatureProcessingDefinition(
    id="ConstructionInstallation",
    target_elements=_make_prefix_variants(
        [
            "uro:ConstructionInstallation",
        ]
    ),
    property_groups=[
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="class",
                    path="./uro:class",
                    datatype="string",
                ),
                Property(
                    name="function",
                    path="./uro:function",
                    datatype="[]string",
                    predefined_codelist="ConstructionInstallation_function",
                ),
                Property(
                    name="usage",
                    path="./uro:usage",
                    datatype="[]string",
                ),
            ],
        )
    ],
    lod_detection=LODDetection(
        lod2=["./uro:lod2Geometry"],
        lod3=["./uro:lod3Geometry"],
        lod4=["./uro:lod4Geometry"],
    ),
    emissions=FeatureEmissions(
        lod2=FeatureEmission(collect_all=[".//uro:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(collect_all=[".//uro:lod3Geometry//gml:Polygon"]),
        lod4=FeatureEmission(collect_all=[".//uro:lod4Geometry//gml:Polygon"]),
    ),
)
