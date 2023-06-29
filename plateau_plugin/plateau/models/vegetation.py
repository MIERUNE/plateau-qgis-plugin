"""植生モデル (./veg/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
)
from .common import facility_id_attribute_attrs

_uro_vegetation_data_quality_attribute = AttributeGroup(
    base_element="./uro:vegetationDataQualityAttribute/uro:VegetationDataQualityAttribute",
    attributes=[
        Attribute(
            name="srcScale",
            path="./uro:srcScale",
            datatype="[]string",
            predefined_codelist="VegetationDataQualityAttribute_srcScale",
        ),
        Attribute(
            name="geometrySrcDesc",
            path="./uro:geometrySrcDesc",
            datatype="[]string",
            predefined_codelist="VegetationDataQualityAttribute_GeometrySrcDesc",
        ),
        Attribute(
            name="thematicSrcDesc",
            path="./uro:thematicSrcDesc",
            datatype="[]string",
            predefined_codelist="VegetationDataQualityAttribute_thematicSrcDesc",
        ),
        Attribute(
            name="appearanceSrcDesc",
            path="./uro:appearanceSrcDesc",
            datatype="[]string",
            predefined_codelist="VegetationDataQualityAttribute_appearanceSrcDesc",
        ),
    ],
)

SOLITARY_VEGETATION_OBJECT = FeatureProcessingDefinition(
    id="SolitaryVegetationObject",
    target_elements=["veg:SolitaryVegetationObject"],
    lod_detection=LODDetection(
        lod1=["./veg:lod1Geometry"],
        lod2=["./veg:lod2Geometry"],
        lod3=["./veg:lod3Geometry"],
    ),
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./veg:class",
                    datatype="string",
                    predefined_codelist="SolitaryVegetationObject_class",
                ),
                Attribute(
                    name="function",
                    path="./veg:function",
                    datatype="string",
                    predefined_codelist="SolitaryVegetationObject_function",
                ),
                Attribute(
                    name="height",
                    path="./veg:height",
                    datatype="double",
                ),
                Attribute(
                    name="trunkDiameter",
                    path="./veg:trunkDiameter",
                    datatype="double",
                ),
                Attribute(
                    name="crownDiameter",
                    path="./veg:crownDiameter",
                    datatype="double",
                ),
            ],
        ),
        _uro_vegetation_data_quality_attribute,
        AttributeGroup(
            base_element="./uro:vegFacilityIdAttribute/uro:FacilityIdAttribute",
            attributes=facility_id_attribute_attrs,
        ),
        # TODO: uro:vegFacilityTypeAttribute
        # TODO: uro:vegFacilityAttribute
        # TODO: uro:vegDmAttribute
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(collect_all=["./veg:lod1Geometry//gml:Polygon"]),
        lod2=FeatureEmission(collect_all=["./veg:lod2Geometry//gml:Polygon"]),
        lod3=FeatureEmission(collect_all=["./veg:lod3Geometry//gml:Polygon"]),
    ),
)

PLANT_COVER = FeatureProcessingDefinition(
    id="PlantCover",
    target_elements=["veg:PlantCover"],
    lod_detection=LODDetection(
        lod1=["./veg:lod1MultiSolid", "./veg:lod1MultiSurface"],
        lod2=["./veg:lod2MultiSolid", "./veg:lod2MultiSurface"],
        lod3=["./veg:lod3MultiSolid", "./veg:lod3MultiSurface"],
    ),
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./veg:class",
                    datatype="string",
                    predefined_codelist="PlantCover_class",
                ),
                Attribute(
                    name="avarageHeight",
                    path="./veg:averageHeight",
                    datatype="double",
                ),
            ],
        ),
        _uro_vegetation_data_quality_attribute,
        AttributeGroup(
            base_element="./uro:vegFacilityIdAttribute/uro:FacilityIdAttribute",
            attributes=facility_id_attribute_attrs,
        ),
        # TODO: uro:vegFacilityTypeAttribute
        # TODO: uro:vegFacilityAttribute
        # TODO: uro:vegDmAttribute
    ],
    emissions=FeatureEmissions(
        lod1=FeatureEmission(
            collect_all=[
                "./veg:lod1MultiSolid//gml:Polygon",
                "./veg:lod1MultiSurface//gml:Polygon",
            ]
        ),
        lod2=FeatureEmission(
            collect_all=[
                "./veg:lod1MultiSolid//gml:Polygon",
                "./veg:lod2MultiSurface//gml:Polygon",
            ]
        ),
        lod3=FeatureEmission(
            collect_all=[
                "./veg:lod1MultiSolid//gml:Polygon",
                "./veg:lod3MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
