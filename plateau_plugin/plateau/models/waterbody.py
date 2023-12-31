"""水辺モデル (./wtr/) および 災害リスク (浸水) モデル (./fld/, ./htd/, ./ifld/, ./tnm/)"""

from .base import (
    Attribute,
    AttributeGroup,
    FacilityAttributePaths,
    FeatureProcessingDefinition,
    GeometricAttribute,
    GeometricAttributes,
)

WATER_BODY = FeatureProcessingDefinition(
    id="wtr:WaterBody",
    name="WaterBody",
    target_elements=[
        "wtr:WaterBody",
    ],
    load_generic_attributes=True,
    attribute_groups=[
        AttributeGroup(
            base_element=None,
            attributes=[
                Attribute(
                    name="class",
                    path="./wtr:class",
                    datatype="string",
                    predefined_codelist="WaterBody_class",
                ),
                Attribute(
                    name="function",
                    path="./wtr:function",  # 浸水リスクモデルで使われる
                    datatype="[]string",
                    predefined_codelist="WaterBody_function",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./uro:waterBodyDetailAttribute/uro:WaterBodyDetailAttribute",
            attributes=[
                Attribute(
                    name="adminType",
                    path="./uro:adminType",
                    datatype="string",
                    predefined_codelist="WaterbodyDetailAttribute_adminType",
                ),
                Attribute(
                    name="area",
                    path="./uro:area",
                    datatype="double",
                ),
                Attribute(
                    name="city",
                    path="./uro:city",
                    datatype="[]string",
                    predefined_codelist="Common_localPublicAuthorities",
                ),
                Attribute(
                    name="flowDirection",
                    path="./uro:flowDirection",
                    datatype="boolean",
                ),
                Attribute(
                    name="kana",
                    path="./uro:kana",
                    datatype="string",
                ),
                Attribute(
                    name="maximumDepth",
                    path="./uro:maximumDepth",
                    datatype="double",
                ),
                Attribute(
                    name="measurementYearMonth",
                    path="./uro:measurementYearMonth",
                    datatype="string",
                ),
                Attribute(
                    name="prefecture",
                    path="./uro:prefecture",
                    datatype="[]string",
                    predefined_codelist="Common_localPublicAuthorities",
                ),
                Attribute(
                    name="riverCode",
                    path="./uro:riverCode",
                    datatype="string",
                    predefined_codelist=None,
                ),
                Attribute(
                    name="waterSurfaceElevation",
                    path="./uro:waterSurfaceElevation",
                    datatype="double",
                ),
                Attribute(
                    name="waterSystemCode",
                    path="./uro:waterSystemCode",
                    datatype="string",
                    predefined_codelist=None,
                ),
            ],
        ),
        AttributeGroup(
            base_element="./uro:floodingRiskAttribute/uro:WaterBodyRiverFloodingRiskAttribute",
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
                    predefined_codelist="RiverFloodingRiskAttribute_rank",
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
                    predefined_codelist="RiverFloodingRiskAttribute_adminType",
                ),
                Attribute(
                    name="scale",
                    path="./uro:scale",
                    datatype="string",
                    predefined_codelist="RiverFloodingRiskAttribute_scale",
                ),
                Attribute(
                    name="duration",
                    path="./uro:duration",
                    datatype="double",
                ),
            ],
        ),
        AttributeGroup(
            base_element="./uro:floodingRiskAttribute/uro:WaterBodyHighTideRiskAttribute",
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
                    predefined_codelist="HighTideRiskAttribute_rank",
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
        ),
        AttributeGroup(
            base_element="./uro:floodingRiskAttribute/uro:WaterBodyTsunamiRiskAttribute",
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
                    predefined_codelist="TsunamiRiskAttribute_rank",
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
        ),
        AttributeGroup(
            base_element="./uro:floodingRiskAttribute/uro:WaterBodyHighTideRiskAttribute",
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
                    predefined_codelist="HighTideRiskAttribute_rank",
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
        ),
        AttributeGroup(
            base_element="./uro:floodingRiskAttribute/uro:WaterBodyInlandFloodingRiskAttribute",
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
                    predefined_codelist="InlandFloodingRiskAttribute_rank",
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
        ),
    ],
    dm_attr_container_path="./uro:wtrDmAttribute",
    facility_attr_paths=FacilityAttributePaths(
        facility_id="./uro:wtrFacilityIdAttribute",
        facility_types="./uro:wtrFacilityTypeAttribute",
        facility_attrs="./uro:wtrFacilityAttribute",
    ),
    geometries=GeometricAttributes(
        lod0=GeometricAttribute(
            is2d=True,
            lod_detection=["./wtr:lod0MultiCurve"],
            collect_all=["./wtr:lod0MultiCurve//gml:LineString"],
        ),
        lod1=GeometricAttribute(
            lod_detection=["./wtr:lod1MultiSurface"],
            collect_all=["./wtr:lod1MultiSurface//gml:Polygon"],
        ),
        lod2=GeometricAttribute(
            lod_detection=["./wtr:lod2Solid"],
            collect_all=[".//wtr:lod2Surface//gml:Polygon"],
            only_direct=["./wtr:lod2Solid//gml:Polygon"],
        ),
        lod3=GeometricAttribute(
            lod_detection=["./wtr:lod3Solid"],
            collect_all=[".//wtr:lod3Surface//gml:Polygon"],
            only_direct=["./wtr:lod3Solid//gml:Polygon"],
        ),
        semantic_parts=[
            ".//wtr:WaterSurface",
            ".//wtr:WaterGroundSurface",
            ".//wtr:WaterClosureSurface",
        ],
    ),
)

WATER_BOUNDARY_SURFACE = FeatureProcessingDefinition(
    id="wtr:_BoundarySurface",
    name="BoundarySurface",
    target_elements=[
        "wtr:WaterSurface",
        "wtr:WaterGroundSurface",
        "wtr:WaterClosureSurface",
    ],
    attribute_groups=[],
    geometries=GeometricAttributes(
        lod2=GeometricAttribute(
            lod_detection=["./wtr:lod2Surface"],
            collect_all=[
                "./wtr:lod2Surface//gml:Polygon",
            ],
        ),
        lod3=GeometricAttribute(
            lod_detection=["./wtr:lod3Surface"],
            collect_all=[
                "./wtr:lod3Surface//gml:Polygon",
            ],
        ),
    ),
)
