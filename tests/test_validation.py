"""プロセッサ定義や入力データの検証 (ValueError) のテスト"""

from types import SimpleNamespace

import lxml.etree as et
import pytest
from qgis.core import QgsCoordinateReferenceSystem, QgsProject

from plateau_plugin.algorithms.utils.layermanger import LayerManager
from plateau_plugin.plateau.models.base import (
    Attribute,
    AttributeGroup,
    FeatureProcessingDefinition,
    GeometricAttributes,
    ProcessorRegistory,
)
from plateau_plugin.plateau.namespaces import BASE_NS
from plateau_plugin.plateau.parse.appearance import parse_appearances
from plateau_plugin.plateau.types import get_table_definition


def _processor(
    id_: str = "p",
    targets: tuple[str, ...] = ("bldg:Building",),
    groups: tuple[AttributeGroup, ...] = (),
    **kwargs,
) -> FeatureProcessingDefinition:
    kwargs.setdefault("geometries", GeometricAttributes())
    return FeatureProcessingDefinition(
        id=id_,
        name=id_,
        target_elements=list(targets),
        attribute_groups=list(groups),
        **kwargs,
    )


def _group(*attrs: Attribute) -> AttributeGroup:
    return AttributeGroup(base_element=None, attributes=attrs)


# --- ProcessorRegistory ---


def test_register_duplicate_id():
    registry = ProcessorRegistory([_processor("a", ("bldg:Building",))])
    with pytest.raises(ValueError, match="Processor id a is already registered"):
        registry.register_processor(_processor("a", ("bldg:Room",)))


def test_register_duplicate_target_in_a_processor():
    with pytest.raises(ValueError, match="Duplicate target element"):
        ProcessorRegistory([_processor("a", ("bldg:Building", "bldg:Building"))])


def test_register_target_of_another_processor():
    with pytest.raises(ValueError, match="bldg:Building is already registered"):
        ProcessorRegistory(
            [_processor("a", ("bldg:Building",)), _processor("b", ("bldg:Building",))]
        )


def test_validate_processors():
    attr = Attribute(
        name="measuredHeight", path="bldg:measuredHeight", datatype="double"
    )
    registry = ProcessorRegistory(
        [
            _processor("a", ("bldg:Building",), (_group(attr),)),
            _processor("b", ("bldg:Room",)),
        ]
    )
    registry.validate_processors()


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param(
            {"nested_attributes": ["bldg:Building/bldg:Missing"]},
            id="nested_attributes",
        ),
        pytest.param(
            {
                "geometries": GeometricAttributes(
                    semantic_parts=["bldg:Building/bldg:Missing"]
                )
            },
            id="semantic_parts",
        ),
    ],
)
def test_validate_processors_unregistered_element(kwargs):
    registry = ProcessorRegistory([_processor("a", ("bldg:Building",), **kwargs)])
    with pytest.raises(ValueError, match="bldg:Missing is not registered"):
        registry.validate_processors()


def test_validate_processors_attribute_name_not_in_path():
    attr = Attribute(name="foo", path="bldg:bar", datatype="string")
    registry = ProcessorRegistory([_processor("a", groups=(_group(attr),))])
    with pytest.raises(ValueError, match="foo not in bldg:bar"):
        registry.validate_processors()


# --- get_table_definition ---


def test_table_definition_same_name_same_datatype():
    attr = Attribute(name="a", path="bldg:a", datatype="string")
    cityobj = SimpleNamespace(processor=_processor(groups=(_group(attr), _group(attr))))
    fields = get_table_definition(cityobj).fields  # type: ignore
    assert [f.name for f in fields].count("a") == 1


def test_table_definition_same_name_different_datatype():
    a1 = Attribute(name="a", path="bldg:a", datatype="string")
    a2 = Attribute(name="a", path="bldg:a", datatype="integer")
    cityobj = SimpleNamespace(processor=_processor(groups=(_group(a1), _group(a2))))
    with pytest.raises(ValueError, match="a, string != integer"):
        get_table_definition(cityobj)  # type: ignore


# --- LayerManager ---


def test_layer_requires_geometry_when_lod_is_set(qgis_app):
    manager = LayerManager(
        force2d=False,
        crs=QgsCoordinateReferenceSystem("EPSG:6697"),
        append_mode=False,
        lod_in_name=False,
        project=QgsProject.instance(),
    )
    cityobj = SimpleNamespace(
        processor=SimpleNamespace(id="bldg"), parent=None, lod=1, geometry=None
    )
    with pytest.raises(ValueError, match="bldg has LoD but no geometry"):
        manager.get_layer(cityobj)  # type: ignore


# --- parse_appearances ---


def _appearance_doc(*members: str) -> et._Element:
    body = "".join(
        f"<app:surfaceDataMember>{m}</app:surfaceDataMember>" for m in members
    )
    return et.fromstring(
        f'<core:CityModel xmlns:core="{BASE_NS["core"]}" xmlns:app="{BASE_NS["app"]}">'
        f"<app:appearanceMember><app:Appearance>{body}</app:Appearance></app:appearanceMember>"
        "</core:CityModel>"
    )


def _material(inner: str) -> str:
    return f"<app:X3DMaterial>{inner}</app:X3DMaterial>"


def _texture(ring: str) -> str:
    return (
        "<app:ParameterizedTexture><app:imageURI>tex.jpg</app:imageURI>"
        '<app:target uri="#poly"><app:TexCoordList>'
        f'<app:textureCoordinates ring="{ring}">0 0 1 0 1 1</app:textureCoordinates>'
        "</app:TexCoordList></app:target></app:ParameterizedTexture>"
    )


def test_parse_appearances():
    doc = _appearance_doc(
        _material(
            "<app:diffuseColor>0.1 0.2 0.3</app:diffuseColor>"
            "<app:specularColor>0.4 0.5 0.6</app:specularColor>"
            "<app:emissiveColor>0.7 0.8 0.9</app:emissiveColor>"
            "<app:shininess>0.5</app:shininess>"
            "<app:transparency>0.25</app:transparency>"
            "<app:ambientIntensity>0.75</app:ambientIntensity>"
            "<app:target>#poly1</app:target>"
        ),
        _texture("#ring1"),
    )
    (appearance,) = parse_appearances(doc)
    material = appearance.materials[0]
    assert material.diffuse_color == (0.1, 0.2, 0.3)
    assert material.shininess == 0.5
    assert material.transparency == 0.25
    assert material.ambient_intensity == 0.75
    assert appearance.target_to_material == {"poly1": 0}
    assert appearance.textures[0].image_uri == "tex.jpg"
    texture_idx, uv = appearance.ring_to_texture["ring1"]
    assert texture_idx == 0
    assert uv.shape == (3, 2)


@pytest.mark.parametrize(
    ("member", "message"),
    [
        (
            _material("<app:diffuseColor>0.1 0.2</app:diffuseColor>"),
            "Invalid diffuseColor",
        ),
        (
            _material("<app:specularColor>0.1</app:specularColor>"),
            "Invalid specularColor",
        ),
        (
            _material("<app:emissiveColor>1 2 3 4</app:emissiveColor>"),
            "Invalid emissiveColor",
        ),
        (_material("<app:target>poly1</app:target>"), "Invalid material target"),
        (_texture("ring1"), "Invalid texture ring reference"),
    ],
    ids=["diffuse", "specular", "emissive", "material-target", "texture-ring"],
)
def test_parse_appearances_invalid(member, message):
    with pytest.raises(ValueError, match=message):
        list(parse_appearances(_appearance_doc(member)))
