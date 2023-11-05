from __future__ import annotations

from typing import Iterable

import lxml.etree as et
import numpy as np

from ..types import Geometry, LineStringCollection, PointCollection, PolygonCollection
from .appearance import Appearance


def parse_geometry(  # noqa: C901 (TODO)
    element: et._Element,
    geometry_paths: Iterable[str],
    nsmap: dict[str, str],
    appearance: Appearance | None,
) -> Geometry | None:
    """指定された GML のジオメトリへのパスをもとにマルチパートのジオメトリを構成して返す"""
    # TODO: refactoring

    mpoly_geoms = []
    mpoly_materials: list[int | None] = []
    mpoly_textures: list[int | None] = []
    mpoly_uvs: list[list[np.ndarray] | None] = []
    mline_geoms = []
    mpoint_geoms = []

    for geometry_path in geometry_paths:
        if geometry_path.endswith(("/gml:Polygon", "/gml:Triangle")):
            for polygon in element.iterfind(geometry_path, nsmap):
                # TODO: refactoring
                poly_rings = []
                poly_uvs = []

                # exterior ring
                ring_elem = polygon.find("./gml:exterior/gml:LinearRing", nsmap)
                poslist = ring_elem.find("./gml:posList", nsmap)
                vertices = np.fromstring(poslist.text, dtype=np.float64, sep=" ")
                ring = vertices.reshape(-1, 3)
                poly_rings.append(ring)
                if appearance:
                    poly_id = polygon.get("{http://www.opengis.net/gml}id")
                    ring_id = ring_elem.get("{http://www.opengis.net/gml}id")

                    # TODO: refactoring
                    mat = None
                    if poly_id and (m := appearance.target_to_material.get(poly_id)):
                        mat = m
                    else:
                        sur = polygon.getparent().getparent()
                        sur_id = sur.get("{http://www.opengis.net/gml}id")
                        if sur_id and (m := appearance.target_to_material.get(sur_id)):
                            mat = m
                        elif sur.tag == "{http://www.opengis.net/gml}CompositeSurface":
                            sur2 = sur.getparent().getparent()
                            sur2_id = sur2.get("{http://www.opengis.net/gml}id")
                            if sur2_id and (
                                m := appearance.target_to_material.get(sur2_id)
                            ):
                                mat = m

                    mpoly_materials.append(mat)

                    if tex_uv := appearance.ring_to_texture.get(ring_id):
                        tex, uv = tex_uv
                        assert ring.shape[0] == uv.shape[0]
                        mpoly_textures.append(tex)
                        poly_uvs.append(uv)
                    else:
                        mpoly_textures.append(None)
                        poly_uvs.append(None)

                # interior rings
                for ring_elem in polygon.iterfind(
                    "./gml:interior/gml:LinearRing", nsmap
                ):
                    poslist = ring_elem.find("./gml:posList", nsmap)
                    vertices = np.fromstring(poslist.text, dtype=np.float64, sep=" ")
                    ring = vertices.reshape(-1, 3)
                    poly_rings.append(ring)
                    if appearance:
                        uv = None
                        ring_id = ring_elem.get("{http://www.opengis.net/gml}id")
                        if tex_uv := appearance.ring_to_texture.get(ring_id):
                            _, uv = tex_uv
                            poly_uvs.append(uv)

                if appearance:
                    mpoly_uvs.append(poly_uvs)
                mpoly_geoms.append(poly_rings)

        elif geometry_path.endswith("/gml:LineString"):
            for linestring in element.iterfind(geometry_path, nsmap):
                poslist = linestring.find("./gml:posList", nsmap)
                vertices = np.fromstring(poslist.text, dtype=np.float64, sep=" ")
                line = vertices.reshape(-1, 3)
                mline_geoms.append(line)

        elif geometry_path.endswith("/gml:Point"):
            # TODO
            pass

        elif geometry_path.endswith("/uro:pos"):
            # TODO pos
            pass

        else:
            raise NotImplementedError(f"Unsupported geometry path: {geometry_path}")

    if mpoly_geoms:
        if appearance:
            assert len(mpoly_geoms) == len(mpoly_textures)
            assert len(mpoly_geoms) == len(mpoly_uvs)
            assert len(mpoly_geoms) == len(mpoly_materials)
        return PolygonCollection(
            polygons=mpoly_geoms,
            materials=mpoly_materials if appearance else None,
            textures=mpoly_textures if appearance else None,
            uvs=mpoly_uvs if appearance else None,
        )
    elif mline_geoms:
        return LineStringCollection(lines=mline_geoms)
    elif mpoint_geoms:
        return PointCollection(points=np.vstack(mpoint_geoms))

    return None
