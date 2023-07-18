"""都市設備モデル (./fur/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FacilityAttributePaths,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)

CITY_FURNITURE = FeatureProcessingDefinition(
    id="frn:CityFurniture",
    name="CityFurniture",
    target_elements=["frn:CityFurniture"],
    load_generic_attributes=True,
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
        # # FIXME: cityFurnitureDetailAttribute は多重度が[0..*] (入れ子) なのでこれは正しくない
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
