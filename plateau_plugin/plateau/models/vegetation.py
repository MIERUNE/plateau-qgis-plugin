"""植生モデル (./veg/)"""

from .base import (
    FeatureEmission,
    FeatureEmissions,
    FeatureProcessingDefinition,
    LODDetection,
    Property,
    PropertyGroup,
)

_uro_vegetation_data_quality_attribute = PropertyGroup(
    base_element="./uro:vegetationDataQualityAttribute/uro:VegetationDataQualityAttribute",
    properties=[
        Property(
            name="uro:srcScale",
            path="./uro:srcScale",
            datatype="[]string",
            predefined_codelist="VegetationDataQualityAttribute_srcScale",
        ),
        Property(
            name="uro:geometrySrcDesc",
            path="./uro:geometrySrcDesc",
            datatype="[]string",
            predefined_codelist="VegetationDataQualityAttribute_GeometrySrcDesc",
        ),
        Property(
            name="uro:thematicSrcDesc",
            path="./uro:thematicSrcDesc",
            datatype="[]string",
            predefined_codelist="VegetationDataQualityAttribute_thematicSrcDesc",
        ),
        Property(
            name="uro:appearanceSrcDesc",
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
    property_groups=[
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="class",
                    path="./veg:class",
                    datatype="string",
                    predefined_codelist="SolitaryVegetationObject_class",
                ),
                Property(
                    name="function",
                    path="./veg:function",
                    datatype="string",
                    predefined_codelist="SolitaryVegetationObject_function",
                ),
                Property(
                    name="height",
                    path="./veg:height",
                    datatype="double",
                ),
                Property(
                    name="trunkDiameter",
                    path="./veg:trunkDiameter",
                    datatype="double",
                ),
                Property(
                    name="crownDiameter",
                    path="./veg:crownDiameter",
                    datatype="double",
                ),
            ],
        ),
        # uro:VegetationDataQualityAttribute
        _uro_vegetation_data_quality_attribute,
        # TODO:
        # uro:vegFacilityTypeAttribute
        # uro:vegFacilityIdAttribute
        # uro:vegFacilityAttribute
        # uro:vegDmAttribute
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
    property_groups=[
        PropertyGroup(
            base_element=None,
            properties=[
                Property(
                    name="class",
                    path="./veg:class",
                    datatype="string",
                    predefined_codelist="PlantCover_class",
                ),
                Property(
                    name="avarageHeight",
                    path="./veg:averageHeight",
                    datatype="double",
                ),
            ],
        ),
        # uro:VegetationDataQualityAttribute
        _uro_vegetation_data_quality_attribute,
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
