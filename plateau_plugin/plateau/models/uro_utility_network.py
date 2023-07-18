"""地下埋設物モデル (./unf/)

Featureの継承関係:

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
    FacilityAttributePaths,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)

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
    # AttributeGroup(
    #     base_element="./uro:cityFurnitureDetailAttribute/uro:CityFurnitureDetailAttribute",
    #     attributes=[
    #         Attribute(
    #             name="facilityType",
    #             path="./uro:facilityType",
    #             datatype="string",
    #         ),
    #         Attribute(
    #             name="description",
    #             path="./uro:description",
    #             datatype="string",
    #         ),
    #     ],
    # ),
]


UTILITY_NODE = FeatureProcessingDefinition(
    id="uro:UtilityNode",
    name="UtilityNode",
    target_elements=[
        "uro:Appurtenance",
    ],
    load_generic_attributes=True,
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
    dm_attr_container_path="./uro:frnDmAttribute",
    facility_attr_paths=FacilityAttributePaths(
        facility_id="./uro:frnFacilityIdAttribute",
        facility_types="./uro:frnFacilityTypeAttribute",
        facility_attrs="./uro:frnFacilityAttribute",
    ),
    geometries=GeometricAttributes(
        lod1=GeometricAttribute(
            lod_detection=["./frn:lod1Geometry"],
            collect_all=["./frn:lod1Geometry//gml:Polygon"],
        ),
        lod2=GeometricAttribute(
            lod_detection=["./frn:lod2Geometry"],
            collect_all=["./frn:lod2Geometry//gml:Polygon"],
        ),
        lod3=GeometricAttribute(
            lod_detection=["./frn:lod3Geometry"],
            collect_all=["./frn:lod3Geometry//gml:Polygon"],
        ),
    ),
)

UTILITY_NODE_CONTAINER = FeatureProcessingDefinition(
    id="uro:UtilityNodeContainer",
    name="UtilityNodeContainer",
    target_elements=[
        "uro:Manhole",
        "uro:Handhole",
    ],
    load_generic_attributes=True,
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
    dm_attr_container_path="./uro:frnDmAttribute",
    facility_attr_paths=FacilityAttributePaths(
        facility_id="./uro:frnFacilityIdAttribute",
        facility_types="./uro:frnFacilityTypeAttribute",
        facility_attrs="./uro:frnFacilityAttribute",
    ),
    geometries=GeometricAttributes(
        lod1=GeometricAttribute(
            lod_detection=["./frn:lod1Geometry"],
            collect_all=["./frn:lod1Geometry//gml:Polygon"],
        ),
        lod2=GeometricAttribute(
            lod_detection=["./frn:lod2Geometry"],
            collect_all=["./frn:lod2Geometry//gml:Polygon"],
        ),
        lod3=GeometricAttribute(
            lod_detection=["./frn:lod3Geometry"],
            collect_all=["./frn:lod3Geometry//gml:Polygon"],
        ),
    ),
)

UTILITY_LINK = FeatureProcessingDefinition(
    id="uro:UtilityLink",
    name="UtilityLink",
    target_elements=[
        "uro:Pipe",
        "uro:WaterPipe",
        "uro:ThermalPipe",
        "uro:SewerPipe",
        "uro:OilGasChemicalsPipe",
        "uro:Duct",
        "uro:Cable",
        "uro:TelecommunicationsCable",
        "uro:ElectricityCable",
    ],
    load_generic_attributes=True,
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
    dm_attr_container_path="./uro:frnDmAttribute",
    facility_attr_paths=FacilityAttributePaths(
        facility_id="./uro:frnFacilityIdAttribute",
        facility_types="./uro:frnFacilityTypeAttribute",
        facility_attrs="./uro:frnFacilityAttribute",
    ),
    geometries=GeometricAttributes(
        lod1=GeometricAttribute(
            lod_detection=["./frn:lod1Geometry"],
            collect_all=["./frn:lod1Geometry//gml:Polygon"],
        ),
        lod2=GeometricAttribute(
            lod_detection=["./frn:lod2Geometry"],
            collect_all=["./frn:lod2Geometry//gml:Polygon"],
        ),
        lod3=GeometricAttribute(
            lod_detection=["./frn:lod3Geometry"],
            collect_all=["./frn:lod3Geometry//gml:Polygon"],
        ),
    ),
)
