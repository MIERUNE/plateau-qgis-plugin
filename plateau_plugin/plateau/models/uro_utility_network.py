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
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
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
    AttributeGroup(
        base_element=None,
        attributes=[
            Attribute(
                name="function",
                path="./frn:function",
                datatype="[]string",
                predefined_codelist="CityFurniture_function",
            ),
            Attribute(
                name="occupierName",
                path="./uro:occupierName",
                datatype="string",
            ),
            Attribute(
                name="occupierType",
                path="./uro:occupierType",
                datatype="string",
                predefined_codelist="UtilityNetworkElement_occupierType",
            ),
            Attribute(
                name="year",
                path="./uro:year",
                datatype="integer",
            ),
            Attribute(
                name="yearType",
                path="./uro:yearType",
                datatype="string",
                predefined_codelist="UtilityNetworkElement_yearType",
            ),
        ],
    ),
    # uro:CityFurnitureDataQualityAttribute
    AttributeGroup(
        base_element="./uro:cityFurnitureDataQualityAttribute/uro:CityFurnitureDataQualityAttribute",
        attributes=[
            Attribute(
                name="srcScale",
                path="./uro:srcScale",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_srcScale",
            ),
            Attribute(
                name="geometrySrcDesc",
                path="./uro:geometrySrcDesc",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_geometrySrcDesc",
            ),
            Attribute(
                name="thematicSrcDesc",
                path="./uro:thematicSrcDesc",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_thematicSrcDesc",
            ),
            Attribute(
                name="appearanceSrcDesc",
                path="./uro:appearanceSrcDesc",
                datatype="[]string",
                predefined_codelist="CityFurnitureDataQualityAttribute_appearanceSrcDesc",
            ),
            Attribute(
                name="lodType",
                path="./uro:lodType",
                datatype="[]string",
            ),
        ],
    ),
    # FIXME: cityFurnitureDetailAttribute は多重度が[0..*] (入れ子)
    AttributeGroup(
        base_element="./uro:cityFurnitureDetailAttribute/uro:CityFurnitureDetailAttribute",
        attributes=[
            Attribute(
                name="facilityType",
                path="./uro:facilityType",
                datatype="string",
            ),
            Attribute(
                name="description",
                path="./uro:description",
                datatype="string",
            ),
        ],
    ),
    AttributeGroup(
        base_element="./uro:frnFacilityIdAttribute/uro:FacilityIdAttribute",
        attributes=facility_id_attribute_attrs,
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
    attribute_groups=[
        *_common_property_groups,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="appurtenanceType",
                    path="./uro:appurtenanceType",
                    datatype="string",
                    predefined_codelist="Appurtenance_appurtenanceType",
                ),
                Attribute(
                    name="nextLink",
                    path="./uro:nextLink",
                    datatype="[]string",
                ),
                Attribute(
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
    attribute_groups=[
        *_common_property_groups,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="appurtenance",
                    path="./uro:appurtenance",
                    datatype="[]string",
                ),
                Attribute(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
                Attribute(
                    name="innerDiamiterLong",
                    path="./uro:innerDiamiterLong",
                    datatype="double",
                ),
                Attribute(
                    name="innerDiamiterShort",
                    path="./uro:innerDiamiterShort",
                    datatype="double",
                ),
                Attribute(
                    name="outerDiamiterLong",
                    path="./uro:outerDiamiterLong",
                    datatype="double",
                ),
                Attribute(
                    name="outerDiamiterShort",
                    path="./uro:outerDiamiterShort",
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
    attribute_groups=[
        *_common_property_groups,
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="cables",
                    path="./uro:cables",
                    datatype="integer",
                ),
                Attribute(
                    name="columns",
                    path="./uro:columns",
                    datatype="integer",
                ),
                Attribute(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
                Attribute(
                    name="endNode",
                    path="./uro:endNode",
                    datatype="string",
                ),
                Attribute(
                    name="horizontalLength",
                    path="./uro:horizontalLength",
                    datatype="double",
                ),
                Attribute(
                    name="innerDiamiter",
                    path="./uro:innerDiamiter",
                    datatype="double",
                ),
                Attribute(
                    name="length",
                    path="./uro:length",
                    datatype="double",
                ),
                Attribute(
                    name="material",
                    path="./uro:material",
                    datatype="string",
                    predefined_codelist=None,
                ),
                Attribute(
                    name="maxDepth",
                    path="./uro:maxDepth",
                    datatype="double",
                ),
                Attribute(
                    name="minDepth",
                    path="./uro:minDepth",
                    datatype="double",
                ),
                Attribute(
                    name="offset",
                    path="./uro:offset",
                    datatype="double",
                ),
                Attribute(
                    name="outerDiamiter",
                    path="./uro:outerDiamiter",
                    datatype="double",
                ),
                Attribute(
                    name="rows",
                    path="./uro:rows",
                    datatype="integer",
                ),
                Attribute(
                    name="sewerWaterType",
                    path="./uro:sewerWaterType",
                    datatype="string",
                    predefined_codelist=None,
                ),
                Attribute(
                    name="sleeveType",
                    path="./uro:sleeveType",
                    datatype="double",
                ),
                Attribute(
                    name="startNode",
                    path="./uro:startNode",
                    datatype="string",
                ),
                Attribute(
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
