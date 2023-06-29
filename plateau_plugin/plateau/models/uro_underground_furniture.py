"""地下埋設物モデル (./unf/)"""

# FIXME:
# TODO: 以下、fur:CityFurniture 用の定義をコピペしただけなので、内容は要検証

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


# TODO: 種別ごと (Pipe, Cable, etc.) に分けたほうがよさそう
UNDERGROUND_CITY_FURNITURE = FeatureProcessingDefinition(
    id="UnderGroundCityFurniture",
    target_elements=_make_prefix_variants(
        [
            "uro:Pipe",
            "uro:WaterPipe",
            "uro:ThermalPipe",
            "uro:SewerPipe",
            "uro:OilGasChemicalPipe",
            "uro:Duct",
            "uro:Cable",
            "uro:TelecommunicationsCable",
            "uro:ElectricityCable",
            "uro:Appurtenance",
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
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="class",
                    path="./frn:class",
                    datatype="string",
                    predefined_codelist="CityFurniture_class",
                ),
                Property(
                    name="function",
                    path="./frn:function",
                    datatype="[]string",
                    predefined_codelist="CityFurniture_function",
                ),
                Property(
                    name="usage",
                    path="./frn:usage",
                    datatype="[]string",
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
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(collect_all=["./frn:lod1Geometry//gml:Polygon"]),
        lod2=FeatureEmission(collect_all=["./frn:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(collect_all=["./frn:lod3Geometry//gml:Polygon"]),
    ),
)
