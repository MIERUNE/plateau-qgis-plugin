"""都市設備モデル (./fur/)"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
    Property,
    PropertyGroup,
)
from .common import facility_id_attribute_attrs

CITY_FURNITURE = FeatureProcessingDefinition(
    id="CityFurniture",
    target_elements=["frn:CityFurniture"],
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
