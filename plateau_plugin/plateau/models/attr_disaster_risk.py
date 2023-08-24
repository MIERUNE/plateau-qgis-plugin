"""災害リスク属性を、ジオメトリなし Feature として処理する"""

from .base import (
    Attribute,
    AttributeGroup,
    FeatureProcessingDefinition,
    GeometricAttributes,
)

ATTR_DISASTER_RISK_RIVER_FLOODING = FeatureProcessingDefinition(
    id="uro:RiverFloodingRisk",
    name="RiverFloodingRisk",
    target_elements=[
        "uro:BuildingRiverFloodingRiskAttribute",
        "uro:RiverFloodingRiskAttribute",
    ],
    non_geometric=True,
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="description",
                    path="./uro:description",
                    datatype="string",
                ),
                Attribute(
                    name="rank",
                    path="./uro:rank",
                    datatype="string",
                    predefined_codelist={
                        "uro:BuildingRiverFloodingRiskAttribute": "BuildingRiverFloodingRiskAttribute_rank",
                        "uro:RiverFloodingRiskAttribute": "RiverFloodingRiskAttribute_rank",
                    },
                ),
                Attribute(
                    name="rankOrg",
                    path="./uro:rankOrg",
                    datatype="string",
                ),
                Attribute(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
                Attribute(
                    name="adminType",
                    path="./uro:adminType",
                    datatype="string",
                    predefined_codelist={
                        "uro:BuildingRiverFloodingRiskAttribute": "BuildingRiverFloodingRiskAttribute_adminType",
                        "uro:RiverFloodingRiskAttribute": "RiverFloodingRiskAttribute_adminType",
                    },
                ),
                Attribute(
                    name="scale",
                    path="./uro:scale",
                    datatype="string",
                    predefined_codelist={
                        "uro:BuildingRiverFloodingRiskAttribute": "BuildingRiverFloodingRiskAttribute_scale",
                        "uro:RiverFloodingRiskAttribute": "RiverFloodingRiskAttribute_scale",
                    },
                ),
                Attribute(
                    name="duration",
                    path="./uro:duration",
                    datatype="double",
                ),
            ],
        )
    ],
    geometries=GeometricAttributes(),
)

ATTR_DISASTER_RISK_TSUNAMI = FeatureProcessingDefinition(
    id="uro:TsunamiRisk",
    name="TsunamiRisk",
    target_elements=[
        "uro:BuildingTsunamiRiskAttribute",
        "uro:TsunamiRiskAttribute",
    ],
    non_geometric=True,
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="description",
                    path="./uro:description",
                    datatype="string",
                ),
                Attribute(
                    name="rank",
                    path="./uro:rank",
                    datatype="string",
                    predefined_codelist={
                        "uro:BuildingTsunamiRiskAttribute": "BuildingTsunamiRiskAttribute_rank",
                        "uro:TsunamiRiskAttribute": "TsunamiRiskAttribute_rank",
                    },
                ),
                Attribute(
                    name="rankOrg",
                    path="./uro:rankOrg",
                    datatype="string",
                ),
                Attribute(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
            ],
        )
    ],
    geometries=GeometricAttributes(),
)

ATTR_DISASTER_RISK_HIGH_TIDE = FeatureProcessingDefinition(
    id="uro:HighTideRisk",
    name="HighTideRisk",
    target_elements=[
        "uro:BuildingHighTideRiskAttribute",
        "uro:HighTideRiskAttribute",
    ],
    non_geometric=True,
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="description",
                    path="./uro:description",
                    datatype="string",
                ),
                Attribute(
                    name="rank",
                    path="./uro:rank",
                    datatype="string",
                    predefined_codelist={
                        "uro:BuildingHighTideRiskAttribute": "BuildingHighTideRiskAttribute_rank",
                        "uro:HighTideRiskAttribute": "HighTideRiskAttribute_rank",
                    },
                ),
                Attribute(
                    name="rankOrg",
                    path="./uro:rankOrg",
                    datatype="string",
                ),
                Attribute(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
            ],
        )
    ],
    geometries=GeometricAttributes(),
)

ATTR_DISASTER_RISK_INLAND_FLOODING = FeatureProcessingDefinition(
    id="uro:InlandFloodingRisk",
    name="InlandFloodingRisk",
    target_elements=[
        "uro:BuildingInlandFloodingRiskAttribute",
        "uro:InlandFloodingRiskAttribute",
    ],
    non_geometric=True,
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="description",
                    path="./uro:description",
                    datatype="string",
                ),
                Attribute(
                    name="rank",
                    path="./uro:rank",
                    datatype="string",
                    predefined_codelist={
                        "uro:BuildingInlandFloodingRiskAttribute": "BuildingInlandFloodingRiskAttribute_rank",
                        "uro:InlandFloodingRiskAttribute": "InlandFloodingRiskAttribute_rank",
                    },
                ),
                Attribute(
                    name="rankOrg",
                    path="./uro:rankOrg",
                    datatype="string",
                ),
                Attribute(
                    name="depth",
                    path="./uro:depth",
                    datatype="double",
                ),
            ],
        )
    ],
    geometries=GeometricAttributes(),
)

ATTR_DISASTER_RISK_LAND_SLIDE = FeatureProcessingDefinition(
    id="uro:LandSlideRisk",
    name="LandSlideRisk",
    target_elements=[
        "uro:BuildingLandSlideRiskAttribute",
        "uro:LandSlideRiskAttribute",
    ],
    non_geometric=True,
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="description",
                    path="./uro:description",
                    datatype="string",
                    predefined_codelist={
                        "uro:BuildingLandSlideRiskAttribute": "BuildingLandSlideRiskAttribute_description",
                        "uro:LandSlideRiskAttribute": "LandSlideRiskAttribute_description",
                    },
                ),
                Attribute(
                    name="areaType",
                    path="./uro:areaType",
                    datatype="double",
                    predefined_codelist={
                        "uro:BuildingLandSlideRiskAttribute": "BuildingLandSlideRiskAttribute_areaType",
                        "uro:LandSlideRiskAttribute": "LandSlideRiskAttribute_areaType",
                    },
                ),
            ],
        )
    ],
    geometries=GeometricAttributes(),
)
