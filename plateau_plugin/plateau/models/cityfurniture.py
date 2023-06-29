"""都市設備モデル (./fur/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
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
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./frn:class",
                    datatype="string",
                    predefined_codelist="CityFurniture_class",
                ),
                Attribute(
                    name="function",
                    path="./frn:function",
                    datatype="[]string",
                    predefined_codelist="CityFurniture_function",
                ),
                Attribute(
                    name="usage",
                    path="./frn:usage",
                    datatype="[]string",
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
        # FIXME: cityFurnitureDetailAttribute は多重度が[0..*] (入れ子) なのでこれは正しくない
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
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(collect_all=["./frn:lod1Geometry//gml:Polygon"]),
        lod2=FeatureEmission(collect_all=["./frn:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(collect_all=["./frn:lod3Geometry//gml:Polygon"]),
    ),
)
