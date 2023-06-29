"""その他の構造物モデル (./cons/)"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
    Property,
    PropertyGroup,
)
from .common import facility_id_attribute_attrs


def _make_prefix_variants(prefixed_names: list[str]) -> list[str]:
    # uro を uro2, uro3 に置換する
    names = []
    for name in prefixed_names:
        assert name.startswith("uro:")
        n = name.split(":")[1]
        names.append("uro2:" + n)
        names.append("uro3:" + n)
    return names


_construction_structure_attribute_attrs = [
    Property(
        name="ceilingHeight",
        path="./uro:ceilingHeight",
        datatype="double",
    ),
    Property(
        name="damCode",
        path="./uro:damCode",
        datatype="string",
        predefined_codelist=None,
    ),
    Property(
        name="depth",
        path="./uro:depth",
        datatype="double",
    ),
    Property(
        name="length",
        path="./uro:length",
        datatype="double",
    ),
    Property(
        name="mainPartLength",
        path="./uro:mainPartLength",
        datatype="double",
    ),
    Property(
        name="structureType",
        path="./uro:structureType",
        datatype="string",
        predefined_codelist="ConstructionStructureAttribute_structureType",
    ),
    Property(
        name="totalWaterStorage",
        path="./uro:totalWaterStorage",
        datatype="double",
    ),
    Property(
        name="volume",
        path="./uro:volume",
        datatype="double",
    ),
    Property(
        name="waveDissipatorLength",
        path="./uro:waveDissipatorLength",
        datatype="double",
    ),
    Property(
        name="width",
        path="./uro:width",
        datatype="double",
    ),
]


OTHER_CONSTRUCTION = FeatureProcessingDefinition(
    id="OtherConstruction",
    target_elements=_make_prefix_variants(["uro:OtherConstruction"]),
    lod_detection=LODDetection(
        lod1=["./uro:lod1Geometry"],
        lod2=["./uro:lod2Geometry"],
        lod3=["./uro:lod3Geometry"],
    ),
    property_groups=[
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="class",
                    path="./uro:class",
                    datatype="string",
                    predefined_codelist="OtherConstruction_class",
                ),
                Property(
                    name="function",
                    path="./uro:function",
                    datatype="[]string",
                    predefined_codelist="OtherConstruction_function",
                ),
                Property(
                    name="dateOfConstruction",
                    path="./uro:dateOfConstruction",
                    datatype="date",
                ),
                Property(
                    name="conditionOfConstruction",
                    path="./uro:conditionOfConstruction/uro:ConditionOfConstructionValue",
                    datatype="string",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./uro:consFacilityIdAttribute/uro:FacilityIdAttribute",
            properties=facility_id_attribute_attrs,
        ),
        PropertyGroup(
            base_element="./uro:consBaseAttribute/uro:ConstructionBaseAttribute",
            properties=[
                Property(
                    name="adminOffice",
                    path="./uro:adminOffice",
                    datatype="string",
                ),
                Property(
                    name="adminType",
                    path="./uro:adminType",
                    datatype="string",
                    predefined_codelist="ConstructionBaseAttribute_adminType",
                ),
                Property(
                    name="administorator",
                    path="./uro:administorator",
                    datatype="string",
                ),
                Property(
                    name="completionYear",
                    path="./uro:completionYear",
                    datatype="integer",
                ),
                Property(
                    name="constructionStartYear",
                    path="./uro:constructionStartYear",
                    datatype="integer",
                ),
                Property(
                    name="facilityAge",
                    path="./uro:facilityAge",
                    datatype="integer",
                ),
                Property(
                    name="installer",
                    path="./uro:installer",
                    datatype="string",
                ),
                Property(
                    name="installerType",
                    path="./uro:installerType",
                    datatype="string",
                    predefined_codelist="ConstructionBaseAttribute_installerType",
                ),
                Property(
                    name="kana",
                    path="./uro:kana",
                    datatype="string",
                ),
                Property(
                    name="operatorType",
                    path="./uro:operatorType",
                    datatype="string",
                    predefined_codelist=None,
                ),
                Property(
                    name="purpose",
                    path="./uro:purpose",
                    datatype="string",
                    predefined_codelist="ConstructionBaseAttribute_purpose",
                ),
                Property(
                    name="specification",
                    path="./uro:specification",
                    datatype="string",
                ),
                Property(
                    name="structureOrdinance",
                    path="./uro:structureOrdinance",
                    datatype="string",
                ),
                Property(
                    name="update",
                    path="./uro:update",
                    datatype="date",
                ),
            ],
        ),
        PropertyGroup(
            base_element="./uro:consStructureAttribute/uro:ConstructionStructureAttribute",
            properties=_construction_structure_attribute_attrs,
        ),
        PropertyGroup(
            base_element="./uro:consStructureAttribute/uro:DamAttribute",
            properties=_construction_structure_attribute_attrs,
        ),
        PropertyGroup(
            base_element="./uro:consStructureAttribute/uro:EmbankmentAttribute",
            properties=_construction_structure_attribute_attrs,
        ),
        PropertyGroup(
            base_element="./uro:consDataQualityAttribute/uro:ConstructionDataQualityAttribute",
            properties=[
                Property(
                    name="appearanceSrcDesc",
                    path="./uro:appearanceSrcDesc",
                    datatype="[]string",
                    predefined_codelist="DataQualityAttribute_appearanceSrcDesc",
                ),
                Property(
                    name="dataAcquisition",
                    path="./uro:dataAcquisition",
                    datatype="string",
                ),
                Property(
                    name="geometrySrcDesc",
                    path="./uro:geometrySrcDesc",
                    datatype="[]string",
                    predefined_codelist="DataQualityAttribute_geometrySrcDesc",
                ),
                Property(
                    name="lod1HeightType",
                    path="./uro:lod1HeightType",
                    datatype="string",
                    predefined_codelist="DataQualityAttribute_lod1HeightType",
                ),
                Property(
                    name="lodType",
                    path="./uro:lodType",
                    datatype="[]string",
                    predefined_codelist="OtherConstruction_lodType",
                ),
                Property(
                    name="photoScale",
                    path="./uro:photoScale",
                    datatype="integer",
                ),
                Property(
                    name="srcScale",
                    path="./uro:srcScale",
                    datatype="string",
                    predefined_codelist="DataQualityAttribute_srcScale",
                ),
                Property(
                    name="thematicSrcDesc",
                    path="./uro:thematicSrcDesc",
                    datatype="[]string",
                    predefined_codelist="DataQualityAttribute_thematicSrcDesc",
                ),
            ],
        ),
        # TODO: 入れ子データ
        # Property(
        #    name="elevation",
        #    path="./uro:elevation",
        #    datatype="[]uro:ElevationPropertyType",
        # ),
        # Property(
        #    name="height",
        #    path="./uro:height",
        #    datatype="[]uro:HeightPropertyType",
        # ),
        # Property(
        #    name="consFacilityAttribute",
        #    path="./uro:consFacilityAttribute",
        #    datatype="[]uro:FacilityAttributePropertyType",
        # ),
        # Property(
        #    name="consFacilityTypeAttribute",
        #    path="./uro:consFacilityTypeAttribute",
        #    datatype="[]uro:FacilityTypeAttributePropertyType",
        # ),
        # Property(
        #    name="consDmAttribute",
        #    path="./uro:consDmAttribute",
        #    datatype="[]uro:DmAttributePropertyType",
        # ),
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
