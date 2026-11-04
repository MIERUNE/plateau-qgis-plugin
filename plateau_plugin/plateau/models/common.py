"""様々なモデルで共通して使われる定義"""

from .base import Attribute, AttributeGroup

# uro:facilityIdAttribute の属性セット
# 未使用
facility_id_attribute_attrs = [
    Attribute(
        name="facilityId:alternativeName",
        path="./uro:alternativeName",
        datatype="[]string",
    ),
    Attribute(
        name="facilityId:branchId",
        path="./uro:branchId",
        datatype="string",
    ),
    Attribute(
        name="facilityId:city",
        path="./uro:city",
        datatype="[]string",
        predefined_codelist="Common_localPublicAuthorities",
    ),
    Attribute(
        name="facilityId:endPost",
        path="./uro:endPost",
        datatype="string",
    ),
    Attribute(
        name="facilityId:id",
        path="./uro:id",
        datatype="string",
    ),
    Attribute(
        name="facilityId:partId",
        path="./uro:partId",
        datatype="string",
    ),
    Attribute(
        name="facilityId:prefecture",
        path="./uro:prefecture",
        datatype="[]string",
        predefined_codelist="Common_localPublicAuthorities",
    ),
    Attribute(
        name="facilityId:route",
        path="./uro:route",
        datatype="string",
    ),
    Attribute(
        name="facilityId:startLat",
        path="./uro:startLat",
        datatype="double",
    ),
    Attribute(
        name="facilityId:startLong",
        path="./uro:startLong",
        datatype="double",
    ),
    Attribute(
        name="facilityId:startPost",
        path="./uro:startPost",
        datatype="string",
    ),
]

# uro:RiverfacilityIdAttribute の属性セット
# (uro:facilityIdAttribute の拡張)
river_facility_id_attribute_attrs = [
    *facility_id_attribute_attrs,  # uro:facilityIdAttribute を拡張する
    Attribute(
        name="facilityId:leftDistance",
        path="./uro:leftDistance",
        datatype="double",
    ),
    Attribute(
        name="facilityId:leftEndDistance",
        path="./uro:leftEndDistance",
        datatype="double",
    ),
    Attribute(
        name="facilityId:leftEndPost",
        path="./uro:leftEndPost",
        datatype="double",
    ),
    Attribute(
        name="facilityId:leftPost",
        path="./uro:leftPost",
        datatype="double",
    ),
    Attribute(
        name="facilityId:leftStartDistance",
        path="./uro:leftStartDistance",
        datatype="double",
    ),
    Attribute(
        name="facilityId:leftStartPost",
        path="./uro:leftStartPost",
        datatype="double",
    ),
    Attribute(
        name="facilityId:rightDistance",
        path="./uro:rightDistance",
        datatype="double",
    ),
    Attribute(
        name="facilityId:rightEndDistance",
        path="./uro:rightEndDistance",
        datatype="double",
    ),
    Attribute(
        name="facilityId:rightEndPost",
        path="./uro:rightEndPost",
        datatype="double",
    ),
    Attribute(
        name="facilityId:rightPost",
        path="./uro:rightPost",
        datatype="double",
    ),
    Attribute(
        name="facilityId:rightStartDistance",
        path="./uro:rightStartDistance",
        datatype="double",
    ),
    Attribute(
        name="facilityId:rightStartPost",
        path="./uro:rightStartPost",
        datatype="double",
    ),
    Attribute(
        name="facilityId:riverCode",
        path="./uro:riverCode",
        datatype="string",
    ),
    Attribute(
        name="facilityId:riverName",
        path="./uro:riverName",
        datatype="string",
    ),
    Attribute(
        name="facilityId:sideType",
        path="./uro:sideType",
        datatype="string",
        predefined_codelist="RiverfacilityIdAttribute_sideType",
    ),
]


def data_quality_attribute(container: str) -> AttributeGroup:
    """i-UR 3.1以降で共通になったデータ品質属性。"""
    # 内蔵の DataQualityAttribute_appearanceSrcDesc は旧版の値で、i-UR 3.1 以降とは
    # コード 2〜4 の意味が異なる。内蔵の表は codeSpace より先に引かれるため指定しない。
    attributes = [
        Attribute(
            name=f"geometrySrcDescLod{lod}",
            path=f"./uro:geometrySrcDescLod{lod}",
            datatype="[]string",
            predefined_codelist="DataQualityAttribute_geometrySrcDesc",
        )
        for lod in range(5)
    ]
    attributes.extend(
        Attribute(
            name=f"appearanceSrcDescLod{lod}",
            path=f"./uro:appearanceSrcDescLod{lod}",
            datatype="[]string",
        )
        for lod in range(5)
    )
    attributes.extend(
        [
            Attribute(
                name="thematicSrcDesc",
                path="./uro:thematicSrcDesc",
                datatype="[]string",
                predefined_codelist="DataQualityAttribute_thematicSrcDesc",
            ),
            Attribute(name="lodType", path="./uro:lodType", datatype="[]string"),
            Attribute(
                name="lod1HeightType",
                path="./uro:lod1HeightType",
                datatype="string",
                predefined_codelist="DataQualityAttribute_lod1HeightType",
            ),
            Attribute(
                name="tranDataAcquisition",
                path="./uro:tranDataAcquisition",
                datatype="string",
            ),
        ]
    )
    attributes.extend(
        Attribute(
            name=f"{kind}Lod{lod}",
            path="./uro:publicSurveyDataQualityAttribute/uro:PublicSurveyDataQualityAttribute/"
            f"uro:{kind}Lod{lod}",
            datatype="string" if kind == "srcScale" else "[]string",
        )
        for kind in ("srcScale", "publicSurveySrcDesc")
        for lod in range(5)
    )
    return AttributeGroup(
        base_element=f"./uro:{container}/uro:DataQualityAttribute",
        attributes=attributes,
    )
