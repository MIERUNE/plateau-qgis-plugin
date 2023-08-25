from typing import Iterable

import lxml.etree as et
import numpy as np

from ..namespaces import BASE_NS as _NS
from ..types import Appearance, Material, Texture


def parse_appearances(doc: et._Element) -> Iterable[Appearance]:
    target_to_material: dict[str, Material] = {}
    ring_to_texture: dict[str, tuple[Texture, np.ndarray]] = {}

    for appearance in doc.iterfind(".//app:appearanceMember/app:Appearance", _NS):
        for material in appearance.iterfind(
            ".//app:surfaceDataMember/app:X3DMaterial", _NS
        ):
            m = Material(
                diffuse_color=None,
                specular_color=None,
                shininess=None,
            )
            if (diffuse := material.find("./app:diffuseColor", _NS)) is not None:
                m.diffuse_color = tuple(float(v) for v in diffuse.text.split())
            if (specular := material.find("./app:specularColor", _NS)) is not None:
                m.specular_color = tuple(float(v) for v in specular.text.split())
            if (shininess := material.find("./app:shininess", _NS)) is not None:
                m.shininess = float(shininess.text)

            for target in material.iterfind("./app:target", _NS):
                assert target.text.startswith("#")
                target_id = target.text[1:]
                target_to_material[target_id] = m

        for texture in appearance.iterfind(
            ".//app:surfaceDataMember/app:ParameterizedTexture", _NS
        ):
            image_uri = texture.find("./app:imageURI", _NS).text
            t = Texture(image_uri=image_uri)
            for target in texture.iterfind("./app:target", _NS):
                coords = target.find(".//app:textureCoordinates", _NS)
                ring_id = coords.get("ring")
                assert ring_id.startswith("#")
                ring_id = ring_id[1:]
                uv = np.fromstring(coords.text, dtype=np.float32, sep=" ")
                ring_to_texture[ring_id] = (t, uv.reshape(-1, 2))

        yield Appearance(target_to_material, ring_to_texture)
