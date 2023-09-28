from typing import Iterable

import lxml.etree as et
import numpy as np

from ..namespaces import BASE_NS as _NS
from ..types import Appearance, Material, Texture


def parse_appearances(doc: et._Element) -> Iterable[Appearance]:  # noqa: C901
    for appearance in doc.iterfind(".//app:appearanceMember/app:Appearance", _NS):
        target_to_material: dict[str, int] = {}
        ring_to_texture: dict[str, tuple[int, np.ndarray]] = {}

        materials: list[Material] = []
        for material in appearance.iterfind(
            ".//app:surfaceDataMember/app:X3DMaterial", _NS
        ):
            m = Material()
            if (diffuse := material.find("./app:diffuseColor", _NS)) is not None:
                v = tuple(float(v) for v in diffuse.text.split())
                assert len(v) == 3
                m.diffuse_color = v
            if (specular := material.find("./app:specularColor", _NS)) is not None:
                v = tuple(float(v) for v in specular.text.split())
                assert len(v) == 3
                m.specular_color = v
            if (emissive := material.find("./app:emissiveColor", _NS)) is not None:
                v = tuple(float(v) for v in emissive.text.split())
                assert len(v) == 3
                m.specular_color = v
            if (shininess := material.find("./app:shininess", _NS)) is not None:
                m.shininess = float(shininess.text)
            if (transparency := material.find("./app:transparency", _NS)) is not None:
                m.transparency = float(transparency.text)
            if (
                ambient_intensity := material.find("./app:ambientIntensity", _NS)
            ) is not None:
                m.ambient_intensity = float(ambient_intensity.text)

            materials.append(m)
            idx = len(materials) - 1
            for target in material.iterfind("./app:target", _NS):
                assert target.text.startswith("#")
                target_id = target.text[1:]
                target_to_material[target_id] = idx

        textures: list[Texture] = []
        for texture in appearance.iterfind(
            ".//app:surfaceDataMember/app:ParameterizedTexture", _NS
        ):
            image_uri = texture.find("./app:imageURI", _NS).text
            t = Texture(image_uri=image_uri)
            textures.append(t)
            idx = len(textures) - 1
            for target in texture.iterfind("./app:target", _NS):
                coords = target.find(".//app:textureCoordinates", _NS)
                ring_id = coords.get("ring")
                assert ring_id.startswith("#")
                ring_id = ring_id[1:]
                uv = np.fromstring(coords.text, dtype=np.float32, sep=" ")
                ring_to_texture[ring_id] = (idx, uv.reshape(-1, 2))

        yield Appearance(
            materials=materials,
            textures=textures,
            target_to_material=target_to_material,
            ring_to_texture=ring_to_texture,
        )
