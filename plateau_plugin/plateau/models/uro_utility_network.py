"""地下埋設物モデル (./unf/)

地物の継承関係:

- (uro:UtilityNetworkElement)
  - (uro:UtilityNode)
    - uro:Appurtenance
  - (uro:UtilityNodeContainer)
    - uro:Manhole
    - uro:Handhole
  - (uro:UtilityLink)
    - uro:Pipe
      - uro:WaterPipe
      - uro:SewerPipe
      - uro:OilGasChemicalsPipe
      - uro:ThermalPipe
    - uro:Cable
      - uro:ElectricityCable
      - uro:TelecommunicationsCable
    - uro:Duct

uro:UtilityNode, uro:UtilityNodeContainer, uro:UtilityLink の3種類に分けて取り扱う
"""

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
    names = []
    for name in prefixed_names:
        assert name.startswith("uro:")
        n = name.split(":")[1]
        names.append("uro2:" + n)
        names.append("uro3:" + n)
    return names


_common_property_groups = [
    PropertyGroup(
        base_element=None,
        properties=[
            Property(
                name="function",
                path="./frn:function",
                datatype="[]string",
                predefined_codelist="CityFurniture_function",
            ),
            Property(
                name="occupierName",
                path="./uro:occupierName",
                datatype="string",
            ),
            Property(
                name="occupierType",
                path="./uro:occupierType",
                datatype="string",
                predefined_codelist="UtilityNetworkElement_occupierType",
            ),
            Property(
                name="year",
                path="./uro:year",
                datatype="integer",
            ),
            Property(
                name="yearType",
                path="./uro:yearType",
                datatype="string",
                predefined_codelist="UtilityNetworkElement_yearType",
            ),
        ],
    ),
    # uro:CityFurnitureDataQualityAttribute
    PropertyGroup(
        base_element="./uro:cityFurnitureDataQualityAttribute/uro:CityFurnitureDataQualityAttribute",
        properties=[
            Property(
                name="srcScale",
                path="./uro:srcScale",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_srcScale",
            ),
            Property(
                name="geometrySrcDesc",
                path="./uro:geometrySrcDesc",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_geometrySrcDesc",
            ),
            Property(
                name="thematicSrcDesc",
                path="./uro:thematicSrcDesc",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_thematicSrcDesc",
            ),
            Property(
                name="appearanceSrcDesc",
                path="./uro:appearanceSrcDesc",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_appearanceSrcDesc",
            ),
            Property(
                name="lodType",
                path="./uro:lodType",
                datatype="[]string",
            ),
        ],
    ),
    # FIXME: cityFurnitureDetailAttribute は多重度が[0..*] (入れ子)
    PropertyGroup(
        base_element="./uro:cityFurnitureDetailAttribute/uro:CityFurnitureDetailAttribute",
        properties=[
            Property(
                name="facilityType",
                path="./uro:facilityType",
                datatype="string",
            ),
            Property(
                name="description",
                path="./uro:description",
                datatype="string",
            ),
        ],
    ),
    PropertyGroup(
        base_element="./uro:frnFacilityIdAttribute/uro:FacilityIdAttribute",
        properties=facility_id_attribute_attrs,
    ),
    # TODO: uro:frnFacilityTypeAttribute
    # TODO: uro:frnFacilityAttribute
    # TODO: uro:frnDmAttribute
]


UTILITY_NODE = FeatureProcessingDefinition(
    id="UtilityNode",
    target_elements=_make_prefix_variants(
        [
            "uro:Appurtenance",
        ]
    ),
    lod_detection=LODDetection(
        lod1=["./frn:lod1Geometry"],
        lod2=["./frn:lod2Geometry"],
        lod3=["./frn:lod3Geometry"],
    ),
    property_groups=[
        *_common_property_groups,
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="appurtenanceType",
                    path="./uro:appurtenanceType",
                    datatype="string",
                    predefined_codelist="Appurtenance_appurtenanceType",
                ),
                Property(
                    name="nextLink",
                    path="./uro:nextLink",
                    datatype="[]string",
                ),
                Property(
                    name="previousLink",
                    path="./uro:previousLink",
                    datatype="[]string",
                ),
            ],
        ),
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(collect_all=["./frn:lod1Geometry//gml:Polygon"]),
        lod2=FeatureEmission(collect_all=["./frn:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(collect_all=["./frn:lod3Geometry//gml:Polygon"]),
    ),
)

UTILITY_NODE_CONTAINER = FeatureProcessingDefinition(
    id="UtilityNodeContainer",
    target_elements=_make_prefix_variants(
        [
            "uro:Manhole",
            "uro:Handhole",
        ]
    ),
    lod_detection=LODDetection(
        lod1=["./frn:lod1Geometry"],
        lod2=["./frn:lod2Geometry"],
        lod3=["./frn:lod3Geometry"],
    ),
    property_groups=[
        *_common_property_groups,
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="appurtenance",
                    path="./uro:appurtenance",
                    datatype="[]string",
                ),
                Property(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
                Property(
                    name="innerDiamiterLong",
                    path="./uro:innerDiamiterLong",
                    datatype="double",
                ),
                Property(
                    name="innerDiamiterShort",
                    path="./uro:innerDiamiterShort",
                    datatype="double",
                ),
            ],
        ),
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(collect_all=["./frn:lod1Geometry//gml:Polygon"]),
        lod2=FeatureEmission(collect_all=["./frn:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(collect_all=["./frn:lod3Geometry//gml:Polygon"]),
    ),
)

UTILITY_LINK = FeatureProcessingDefinition(
    id="UtilityLink",
    target_elements=_make_prefix_variants(
        [
            "uro:Pipe",
            "uro:WaterPipe",
            "uro:ThermalPipe",
            "uro:SewerPipe",
            "uro:OilGasChemicalsPipe",
            "uro:Duct",
            "uro:Cable",
            "uro:TelecommunicationsCable",
            "uro:ElectricityCable",
        ]
    ),
    lod_detection=LODDetection(
        lod1=["./frn:lod1Geometry"],
        lod2=["./frn:lod2Geometry"],
        lod3=["./frn:lod3Geometry"],
    ),
    property_groups=[
        *_common_property_groups,
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="cables",
                    path="./uro:cables",
                    datatype="integer",
                ),
                Property(
                    name="columns",
                    path="./uro:columns",
                    datatype="integer",
                ),
                Property(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
                Property(
                    name="endNode",
                    path="./uro:endNode",
                    datatype="string",
                ),
                Property(
                    name="horizontalLength",
                    path="./uro:horizontalLength",
                    datatype="double",
                ),
                Property(
                    name="innerDiamiter",
                    path="./uro:innerDiamiter",
                    datatype="double",
                ),
                Property(
                    name="length",
                    path="./uro:length",
                    datatype="double",
                ),
                Property(
                    name="material",
                    path="./uro:material",
                    datatype="string",
                    predefined_codelist=None,
                ),
                Property(
                    name="maxDepth",
                    path="./uro:maxDepth",
                    datatype="double",
                ),
                Property(
                    name="minDepth",
                    path="./uro:minDepth",
                    datatype="double",
                ),
                Property(
                    name="offset",
                    path="./uro:offset",
                    datatype="double",
                ),
                Property(
                    name="outerDiamiter",
                    path="./uro:outerDiamiter",
                    datatype="double",
                ),
                Property(
                    name="rows",
                    path="./uro:rows",
                    datatype="integer",
                ),
                Property(
                    name="sewerWaterType",
                    path="./uro:sewerWaterType",
                    datatype="string",
                    predefined_codelist=None,
                ),
                Property(
                    name="sleeveType",
                    path="./uro:sleeveType",
                    datatype="double",
                ),
                Property(
                    name="startNode",
                    path="./uro:startNode",
                    datatype="string",
                ),
                Property(
                    name="width",
                    path="./uro:width",
                    datatype="double",
                ),
            ],
        ),
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(collect_all=["./frn:lod1Geometry//gml:Polygon"]),
        lod2=FeatureEmission(collect_all=["./frn:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(collect_all=["./frn:lod3Geometry//gml:Polygon"]),
    ),
)
