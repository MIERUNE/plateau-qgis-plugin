from typing import Iterable, Optional

import lxml.etree as et
import numpy as np

from .types import Geometry, LineStringCollection, PointCollection, PolygonCollection


def parse_geometry(  # noqa: C901 (TODO)
    element: et._Element, geometry_paths: Iterable[str], nsmap: dict[str, str]
) -> Optional[Geometry]:
    """指定された GML のジオメトリへのパスをもとにマルチパートのジオメトリを構成して返す"""
    polygon_geoms = []
    line_geoms = []
    point_geoms = []

    for geometry_path in geometry_paths:
        if geometry_path.endswith(("/gml:Polygon", "/gml:Triangle")):
            for polygon in element.iterfind(geometry_path, nsmap):
                pos_list = polygon.find("./gml:exterior//gml:posList", nsmap)
                vertices = np.fromstring(pos_list.text, dtype=np.float64, sep=" ")
                exterior = vertices.reshape(-1, 3)
                rings = []
                rings.append(exterior)

                for pos_list in polygon.iterfind("./gml:interior//gml:posList", nsmap):
                    vertices = np.fromstring(pos_list.text, dtype=np.float64, sep=" ")
                    interior = vertices.reshape(-1, 3)
                    rings.append(interior)

                polygon_geoms.append(rings)

        elif geometry_path.endswith("/gml:LineString"):
            for linestring in element.iterfind(geometry_path, nsmap):
                pos_list = linestring.find("./gml:posList", nsmap)
                vertices = np.fromstring(pos_list.text, dtype=np.float64, sep=" ")
                line = vertices.reshape(-1, 3)
                line_geoms.append(line)

        elif geometry_path.endswith("/gml:Point"):
            pass

        else:
            raise NotImplementedError(f"Unsupported geometry path: {geometry_path}")

    if polygon_geoms:
        return PolygonCollection(polygons=polygon_geoms)
    elif line_geoms:
        return LineStringCollection(lines=line_geoms)
    elif point_geoms:
        return PointCollection(points=np.vstack(point_geoms))

    return None
