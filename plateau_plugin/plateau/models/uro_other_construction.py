"""その他の構造物モデル (./cons/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
)
from .common import river_facility_id_attribute_attrs


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
    Attribute(
        name="ceilingHeight",
        path="./uro:ceilingHeight",
        datatype="double",
    ),
    Attribute(
        name="damCode",
        path="./uro:damCode",
        datatype="string",
        predefined_codelist=None,
    ),
    Attribute(
        name="depth",
        path="./uro:depth",
        datatype="double",
    ),
    Attribute(
        name="length",
        path="./uro:length",
        datatype="double",
    ),
    Attribute(
        name="mainPartLength",
        path="./uro:mainPartLength",
        datatype="double",
    ),
    Attribute(
        name="structureType",
        path="./uro:structureType",
        datatype="string",
        predefined_codelist="ConstructionStructureAttribute_structureType",
    ),
    Attribute(
        name="totalWaterStorage",
        path="./uro:totalWaterStorage",
        datatype="double",
    ),
    Attribute(
        name="volume",
        path="./uro:volume",
        datatype="double",
    ),
    Attribute(
        name="waveDissipatorLength",
        path="./uro:waveDissipatorLength",
        datatype="double",
    ),
    Attribute(
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
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./uro:class",
                    datatype="string",
                    predefined_codelist="OtherConstruction_class",
                ),
                Attribute(
                    name="function",
                    path="./uro:function",
                    datatype="[]string",
                    predefined_codelist="OtherConstruction_function",
                ),
                Attribute(
                    name="dateOfConstruction",
                    path="./uro:dateOfConstruction",
                    datatype="date",
                ),
                Attribute(
                    name="conditionOfConstruction",
                    path="./uro:conditionOfConstruction/uro:ConditionOfConstructionValue",
                    datatype="string",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./uro:consFacilityIdAttribute/uro:RiverFacilityIdAttribute",
            attributes=river_facility_id_attribute_attrs,
        ),
        AttributeGroup(
            base_element="./uro:consBaseAttribute/uro:ConstructionBaseAttribute",
            attributes=[
                Attribute(
                    name="adminOffice",
                    path="./uro:adminOffice",
                    datatype="string",
                ),
                Attribute(
                    name="adminType",
                    path="./uro:adminType",
                    datatype="string",
                    predefined_codelist="ConstructionBaseAttribute_adminType",
                ),
                Attribute(
                    name="administorator",
                    path="./uro:administorator",
                    datatype="string",
                ),
                Attribute(
                    name="completionYear",
                    path="./uro:completionYear",
                    datatype="integer",
                ),
                Attribute(
                    name="constructionStartYear",
                    path="./uro:constructionStartYear",
                    datatype="integer",
                ),
                Attribute(
                    name="facilityAge",
                    path="./uro:facilityAge",
                    datatype="integer",
                ),
                Attribute(
                    name="installer",
                    path="./uro:installer",
                    datatype="string",
                ),
                Attribute(
                    name="installerType",
                    path="./uro:installerType",
                    datatype="string",
                    predefined_codelist="ConstructionBaseAttribute_installerType",
                ),
                Attribute(
                    name="kana",
                    path="./uro:kana",
                    datatype="string",
                ),
                Attribute(
                    name="operatorType",
                    path="./uro:operatorType",
                    datatype="string",
                    predefined_codelist=None,
                ),
                Attribute(
                    name="purpose",
                    path="./uro:purpose",
                    datatype="string",
                    predefined_codelist="ConstructionBaseAttribute_purpose",
                ),
                Attribute(
                    name="specification",
                    path="./uro:specification",
                    datatype="string",
                ),
                Attribute(
                    name="structureOrdinance",
                    path="./uro:structureOrdinance",
                    datatype="string",
                ),
                Attribute(
                    name="update",
                    path="./uro:update",
                    datatype="date",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./uro:consStructureAttribute/uro:ConstructionStructureAttribute",
            attributes=_construction_structure_attribute_attrs,
        ),
        AttributeGroup(
            base_element="./uro:consStructureAttribute/uro:DamAttribute",
            attributes=_construction_structure_attribute_attrs,
        ),
        AttributeGroup(
            base_element="./uro:consStructureAttribute/uro:EmbankmentAttribute",
            attributes=_construction_structure_attribute_attrs,
        ),
        AttributeGroup(
            base_element="./uro:consDataQualityAttribute/uro:ConstructionDataQualityAttribute",
            attributes=[
                Attribute(
                    name="appearanceSrcDesc",
                    path="./uro:appearanceSrcDesc",
                    datatype="[]string",
                    predefined_codelist="DataQualityAttribute_appearanceSrcDesc",
                ),
                Attribute(
                    name="dataAcquisition",
                    path="./uro:dataAcquisition",
                    datatype="string",
                ),
                Attribute(
                    name="geometrySrcDesc",
                    path="./uro:geometrySrcDesc",
                    datatype="[]string",
                    predefined_codelist="DataQualityAttribute_geometrySrcDesc",
                ),
                Attribute(
                    name="lod1HeightType",
                    path="./uro:lod1HeightType",
                    datatype="string",
                    predefined_codelist="DataQualityAttribute_lod1HeightType",
                ),
                Attribute(
                    name="lodType",
                    path="./uro:lodType",
                    datatype="[]string",
                    predefined_codelist="OtherConstruction_lodType",
                ),
                Attribute(
                    name="photoScale",
                    path="./uro:photoScale",
                    datatype="integer",
                ),
                Attribute(
                    name="srcScale",
                    path="./uro:srcScale",
                    datatype="string",
                    predefined_codelist="DataQualityAttribute_srcScale",
                ),
                Attribute(
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
    attribute_groups=[],
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
    target_elements=_make_prefix_variants(["uro:ConstructionInstallation"]),
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./uro:class",
                    datatype="string",
                ),
                Attribute(
                    name="function",
                    path="./uro:function",
                    datatype="[]string",
                    predefined_codelist="ConstructionInstallation_function",
                ),
                Attribute(
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
